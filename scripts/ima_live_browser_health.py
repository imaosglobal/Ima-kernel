#!/usr/bin/env python3
"""Bounded live-browser health check for the canonical IMA loop.

This verifies public reachability and security boundaries only. It does not
claim an embedded ChatGPT surface is live; that still requires supported
ChatGPT runtime verification.
"""
from __future__ import annotations
import json
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone

CHECKS = {
    "browserglass_health": "https://ima-browserglass.onrender.com/healthz",
    "browserglass_root": "https://ima-browserglass.onrender.com/",
    "ima_public": "https://imaosglobal.github.io/",
}

def get(url: str, timeout: int = 15):
    req = urllib.request.Request(url, headers={"User-Agent": "IMA-LiveBrowser-Health/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            body = r.read(4096).decode("utf-8", "replace")
            return {"ok": True, "status": r.status, "url": r.geturl(), "body_head": body[:500]}
    except urllib.error.HTTPError as e:
        body = e.read(4096).decode("utf-8", "replace")
        return {"ok": False, "status": e.code, "url": e.geturl(), "body_head": body[:500]}
    except Exception as e:
        return {"ok": False, "error": repr(e)}

def main():
    results = {name: get(url) for name, url in CHECKS.items()}
    results["browserglass_session_without_embed"] = get("https://ima-browserglass.onrender.com/api/session")
    passed = (
        results["browserglass_health"].get("ok") and
        results["browserglass_health"].get("status") == 200 and
        results["browserglass_root"].get("ok") and
        results["ima_public"].get("ok") and
        results["browserglass_session_without_embed"].get("status") in {401, 403}
    )
    record = {
        "schema": "IMA-LIVE-BROWSER-HEALTH-1.0",
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "PASS" if passed else "FAIL",
        "checks": results,
        "truth_boundary": "This check proves public endpoint behavior only; it does not prove ChatGPT MCP rendering, human control, local Termux/Chrome connectivity, Google authentication, or successful consequential actions.",
    }
    print(json.dumps(record, ensure_ascii=False, indent=2))
    raise SystemExit(0 if passed else 1)

if __name__ == "__main__":
    main()
