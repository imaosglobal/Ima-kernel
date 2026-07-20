from pathlib import Path
import json
import time

ROOT = Path(".ima/agi_evolution/runtime")
VISION = Path(".ima/vision/universal_human_flourishing_mission.json")

def create_goal():
    vision = json.loads(VISION.read_text())

    goals = [
        "maintain_runtime",
        "improve_capabilities",
        "validate_modules",
        "expand_product_layer",
    ]

    data = {
        "time": time.time(),
        "priority": "system_stability",
        "vision": vision["mission"],
        "vision_principles": vision["principles"],
        "goals": goals,
        "next_action": goals[0],
        "vision_alignment": "required",
    }

    (ROOT / "goal_state.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False)
    )

    return data


if __name__ == "__main__":
    print(json.dumps(create_goal(), indent=2, ensure_ascii=False))
