#!/usr/bin/env python3
"""Canonical IMA leadership and self-governance gate."""
from pathlib import Path
import json, time, sys

root = Path(__file__).resolve().parent
required = [
    "IMA_LEADERSHIP_CONSTITUTION.md",
    "IMA_SYSTEM_UNIFIED_CONTRACT.json",
    "IMA_HUMANITY_PRINCIPLE.md",
    "IMA_AUTONOMOUS_OPERATING_CONTRACT.md",
]
missing = [p for p in required if not (root / p).exists()]
result = {
    "timestamp": time.time(),
    "status": "PASS" if not missing else "FAIL",
    "missing": missing,
    "checks": {p: (root / p).exists() for p in required},
}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not missing else 1)
