#!/usr/bin/env python3
"""Provider-neutral MCP conformance probe for IMA.

Usage:
  python scripts/mcp_conformance.py
  IMA_MCP_URL=https://.../mcp python scripts/mcp_conformance.py

The script never claims provider/Gemini conformance. It reports only observed
HTTP/JSON-RPC results and exits non-zero on failed required checks.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error
import uuid

DEFAULT_URL = "https://ima-universal-action-core.onrender.com/mcp"
PROTOCOL_VERSION = os.getenv("IMA_MCP_PROTOCOL_VERSION", "2025-06-18")


def post_json(url: str, payload: dict, session_id: str | None = None):
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode("utf-8", "replace")
    except Exception as exc:
        return None, {}, f"{type(exc).__name__}: {exc}"


def parse_json_or_sse(text: str):
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        data_lines = [line[5:] for line in text.splitlines() if line.startswith("data:")]
        if data_lines:
            try:
                return json.loads("\n".join(data_lines))
            except json.JSONDecodeError:
                pass
    return None


def check(label: str, ok: bool, detail: str):
    state = "PASS" if ok else "FAIL"
    print(f"[{state}] {label}: {detail}")
    return ok


def main() -> int:
    url = os.getenv("IMA_MCP_URL", DEFAULT_URL)
    request_id = str(uuid.uuid4())

    initialize = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "ima-mcp-conformance", "version": "1.0.0"},
        },
    }

    print(f"IMA MCP conformance probe: {url}")
    status, headers, raw = post_json(url, initialize)
    ok = check("HTTP initialize", status is not None and 200 <= status < 300,
               f"status={status!r}")
    if not ok:
        print("Observed response:", raw[:1000])
        return 1

    init = parse_json_or_sse(raw)
    ok = check("JSON-RPC initialize response", isinstance(init, dict),
               "parseable JSON/JSON-RPC response")
    if not ok:
        print("Observed response:", raw[:1000])
        return 1

    result = init.get("result", {})
    session_id = headers.get("Mcp-Session-Id") or headers.get("mcp-session-id")
    ok = check("Initialize result", isinstance(result, dict) and "protocolVersion" in result,
               f"protocolVersion={result.get('protocolVersion')!r}")
    if not ok:
        print("Observed response:", json.dumps(init)[:2000])
        return 1

    # MCP requires the client to notify the server that initialization is complete.
    notify = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {},
    }
    status2, _, raw2 = post_json(url, notify, session_id=session_id)
    check("Initialized notification", status2 is not None and 200 <= status2 < 300,
          f"status={status2!r}")

    tools_list = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/list",
        "params": {},
    }
    status3, headers3, raw3 = post_json(url, tools_list, session_id=session_id)
    ok = check("Capability discovery (tools/list)",
               status3 is not None and 200 <= status3 < 300,
               f"status={status3!r}")
    if not ok:
        print("Observed response:", raw3[:2000])
        return 1

    discovered = parse_json_or_sse(raw3)
    tools = ((discovered or {}).get("result") or {}).get("tools")
    ok = check("Capability payload", isinstance(tools, list),
               f"tools={len(tools) if isinstance(tools, list) else 'unavailable'}")
    if not ok:
        print("Observed response:", raw3[:2000])
        return 1

    print("[INFO] Authorization-gated action execution is NOT attempted by this generic probe.")
    print("[INFO] Gemini/provider conformance is NOT established by this script alone.")
    print("[INFO] Record the endpoint, timestamp, client, protocol version and observed results as evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
