#!/usr/bin/env python3

from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parent

STATE_FILES = [
    ROOT / "evolution_plan.json",
    ROOT / "cognitive_pipeline_state.json",
    ROOT / "autonomous_state.json",
    ROOT / "latest_cycle.json",
]

def load_json(path):
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def create_proposals():
    plan = load_json(ROOT / "evolution_plan.json")

    gaps = plan.get("detected_gaps", [])
    priority = plan.get("priority_order", [])

    proposals = []

    for item in gaps:
        capability = item.get("capability")
        goal = item.get("goal")

        proposals.append({
            "capability": capability,
            "goal": goal,
            "status": "PROPOSAL_ONLY",
            "mutation_allowed": False,
            "registration_allowed": False,
            "promotion_allowed": False,
        })

    return {
        "type": "EVOLUTION_PROPOSAL_SET",
        "status": "PROPOSAL_ONLY",
        "priority_order": priority,
        "proposals": proposals,
        "mutation_performed": False,
        "module_created": False,
        "timestamp": time.time(),
    }

def main():
    result = create_proposals()

    output = ROOT / "evolution_proposals.json"

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
