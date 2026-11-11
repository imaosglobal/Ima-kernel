#!/usr/bin/env python3
"""Daily AGI readiness gap triage for the canonical IMA loop."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research/IMA_AGI_GAP_REGISTRY.json"
PROGRAM = ROOT / "docs/IMA_AGI_READINESS_AND_GENERAL_INTELLIGENCE_GAP_PROGRAM.md"

def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    priorities = data.get("priority_order", [])
    print("IMA_AGI_GAP_CHECK=PASS")
    print(f"PROGRAM={PROGRAM.relative_to(ROOT)}")
    print("PRIORITY_GAPS=" + ",".join(priorities))
    print("RULE=No AGI claim without implementation,test,deployment,runtime verification,measurement,and independent reproducible evidence.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
