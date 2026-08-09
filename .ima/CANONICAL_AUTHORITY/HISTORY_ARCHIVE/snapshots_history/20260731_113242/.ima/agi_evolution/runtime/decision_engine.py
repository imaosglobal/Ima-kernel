from pathlib import Path
import json
import time

ROOT = Path(".ima/agi_evolution/runtime")

def decide():
    master = json.loads(
        (ROOT / "ima_master_state.json").read_text()
    )

    goals = json.loads(
        (ROOT / "goal_state.json").read_text()
    )

    decision = {
        "time": time.time(),
        "current": master.get("decision"),
        "next_action": goals.get("next_action"),
        "priority": goals.get("priority"),
        "vision_alignment": goals.get("vision_alignment"),
        "vision_verified": bool(
            goals.get("vision") and
            goals.get("vision_principles")
        ),
    }

    (ROOT / "decision_state.json").write_text(
        json.dumps(decision, indent=2, ensure_ascii=False)
    )

    return decision


if __name__ == "__main__":
    print(json.dumps(decide(), indent=2, ensure_ascii=False))
