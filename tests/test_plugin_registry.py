#!/usr/bin/env python3
"""Contract checks for IMA's plugin capability registry.

The registry is the routing authority. Every routing target must exist as a
registered capability, and candidate targets must be explicitly marked
candidate rather than silently appearing connected.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".ima" / "plugins" / "REGISTRY.json"


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = {item["id"]: item for item in data.get("connected", [])}

    errors: list[str] = []
    for route, targets in data.get("routing", {}).items():
        for target in targets:
            if target not in entries:
                errors.append(f"{route}: unknown routing target {target!r}")
                continue
            status = entries[target].get("status", "connected")
            if status == "candidate" and target.endswith("_candidate") is False:
                errors.append(
                    f"{route}: candidate capability {target!r} must use a *_candidate id"
                )

    for item in data.get("connected", []):
        if item.get("status") == "candidate" and not item["id"].endswith("_candidate"):
            errors.append(f"candidate entry must use *_candidate id: {item['id']!r}")

    if errors:
        print("IMA REGISTRY CONTRACT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "IMA REGISTRY CONTRACT: PASS "
        f"(registered={len(entries)}, routes={len(data.get('routing', {}))})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
