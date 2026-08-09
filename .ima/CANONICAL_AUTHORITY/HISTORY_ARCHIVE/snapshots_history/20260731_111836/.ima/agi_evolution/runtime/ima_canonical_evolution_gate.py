#!/usr/bin/env python3

from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parent
PROPOSALS = ROOT / "evolution_proposals.json"

def main():
    proposals = []

    if PROPOSALS.is_file():
        try:
            data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
            proposals = data.get("proposals", [])
        except Exception:
            proposals = []

    audit = {
        "type": "CANONICAL_EVOLUTION_GATE_AUDIT",
        "status": "NO_PROPOSALS" if not proposals else "PROPOSALS_PENDING_APPROVAL",
        "proposals": proposals,
        "mutation_performed": False,
        "promotion_performed": False,
        "registration_performed": False,
        "timestamp": time.time(),
    }

    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
