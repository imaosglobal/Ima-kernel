#!/usr/bin/env python3
"""Check official world-model availability signals without claiming live provider access."""
from __future__ import annotations
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".ima" / "loop" / "WORLD_MODEL_AVAILABILITY.json"

SOURCES = {
    "genie4_official": "https://deepmind.google/models/genie/",
    "genie4_announcement": "https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/",
    "gemini_api_models": "https://ai.google.dev/api/models",
}

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "IMA-world-model-monitor/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")

def classify(text: str) -> dict:
    low = re.sub(r"\\s+", " ", text.lower())
    return {
        "trusted_tester_preview_signal": "trusted testers" in low,
        "project_genie_signal": "project genie" in low,
        "api_early_access_signal": "early access partners" in low,
        "waitlist_signal": "waitlist" in low,
        "limitations_signal": "limitations" in low,
    }

def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    sources = {}
    errors = {}
    for name, url in SOURCES.items():
        try:
            body = fetch(url)
            sources[name] = {"url": url, "ok": True, "signals": classify(body)}
        except Exception as exc:
            sources[name] = {"url": url, "ok": False}
            errors[name] = repr(exc)

    genie = sources.get("genie4_official", {})
    sig = genie.get("signals", {})
    if not genie.get("ok"):
        status = "NOT_VERIFIED"
    elif sig.get("api_early_access_signal") or sig.get("trusted_tester_preview_signal"):
        status = "ACCESS_REQUIRED"
    else:
        status = "NOT_VERIFIED"

    result = {
        "schema": "IMA-WORLD-MODEL-AVAILABILITY-1.0",
        "checked_at": now,
        "status": status,
        "provider": "Google DeepMind Genie 4",
        "truth_boundary": "Official availability signals do not prove that this IMA deployment has credentials, tester access, or a successful live generation request.",
        "official_sources": sources,
        "errors": errors,
        "next_gate": [
            "obtain authorized Genie 4 / Project Genie / Gemini API access if offered",
            "connect credentials only through a secure deployment secret store",
            "run a bounded low-risk generation request",
            "verify output provenance and device fallback",
            "only then mark VERIFIED_LIVE"
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
