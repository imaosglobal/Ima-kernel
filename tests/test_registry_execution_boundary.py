#!/usr/bin/env python3
"""Regression checks for the registry-to-runtime execution boundary.

Nylas may remain implemented in the source tree while it is a candidate in the
authoritative registry. Candidate status must therefore prevent execution.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
REGISTRY = ROOT / ".ima" / "plugins" / "REGISTRY.json"

PROTECTED_NYLAS_ENDPOINTS = {
    "email_status",
    "email_verify",
    "email_webhook_setup",
    "email_messages",
    "email_monitor_status",
}


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    nylas = next(
        (item for item in registry.get("connected", []) if item.get("provider") == "Nylas"),
        None,
    )
    errors: list[str] = []

    if not nylas:
        errors.append("Nylas registry entry is missing")
    elif nylas.get("status") != "candidate":
        errors.append(
            f"Nylas must remain candidate until explicitly connected and verified; "
            f"found status={nylas.get('status')!r}"
        )

    tree = ast.parse(APP.read_text(encoding="utf-8"))
    functions = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    if "_provider_execution_allowed" not in functions:
        errors.append("app.py is missing the registry execution guard")
    else:
        guard_source = ast.get_source_segment(APP.read_text(encoding="utf-8"), functions["_provider_execution_allowed"]) or ""
        if '== "connected"' not in guard_source:
            errors.append("registry execution guard must allow execution only for connected status")

    for name in PROTECTED_NYLAS_ENDPOINTS:
        node = functions.get(name)
        if node is None:
            errors.append(f"missing protected endpoint function: {name}")
            continue
        calls = [
            call for call in ast.walk(node)
            if isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "_provider_execution_allowed"
        ]
        if not calls:
            errors.append(f"{name} does not enforce the registry execution guard")

    if errors:
        print("IMA REGISTRY EXECUTION BOUNDARY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "IMA REGISTRY EXECUTION BOUNDARY: PASS "
        f"(protected_endpoints={len(PROTECTED_NYLAS_ENDPOINTS)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
