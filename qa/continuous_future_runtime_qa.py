#!/usr/bin/env python3
"""Local, dependency-light QA for IMA continuous-future governance.

Run from the repository root:
    python qa/continuous_future_runtime_qa.py
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ima" / "policies" / "CONTINUOUS_FUTURE_POLICY.json"
REGISTRY = ROOT / ".ima" / "architecture" / "COMPONENT_REGISTRY.json"
SELF_STEWARDSHIP = ROOT / ".ima" / "policies" / "SELF_STEWARDSHIP_POLICY.json"

ENFORCED = {
    "ima_master_runtime.py": "ima_master_runtime",
    "ima_brain.py": "ima_brain",
    "ima_mom.py": "ima_mom",
}


def main() -> int:
    print("=== IMA CONTINUOUS FUTURE QA ===")
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    assert policy["id"] == "IMA-CONTINUOUS-FUTURE-001"
    assert policy["status"] == "active"
    assert policy["principle"]
    assert policy["lifecycle"]
    assert policy["always_apply"]
    stewardship = json.loads(SELF_STEWARDSHIP.read_text(encoding="utf-8"))
    assert stewardship["id"] == "IMA-SELF-STEWARDSHIP-001"
    assert stewardship["status"] == "active"
    assert stewardship["required_loop"]
    assert stewardship["boundaries"]
    print("POLICY: PASS (continuous-future + self-stewardship)")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["policy"] == policy["id"]
    assert registry["self_stewardship_policy"] == stewardship["id"]
    for item in registry["components"]:
        assert (ROOT / item["path"]).exists(), item["path"]
        assert item["role"]
        assert item["depends_on"] is not None
        assert item["next"] is not None
    print(f"REGISTRY: PASS ({len(registry['components'])} components)")

    source_map = {}
    for filename, component in ENFORCED.items():
        path = ROOT / filename
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename)
        assert "enforce_component_contract" in source
        assert component in source
        source_map[filename] = source
    print("SYNTAX: PASS (enforced runtime files)")

    import sys
    sys.path.insert(0, str(ROOT))
    from core.continuous_future import enforce_component_contract

    for component in ENFORCED.values():
        contract = enforce_component_contract(component)
        assert contract["policy_id"] == policy["id"]
    print("ENFORCEMENT: PASS (3 runtime boundaries)")

    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
