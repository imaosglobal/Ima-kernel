import json
from pathlib import Path

STATE=Path(".ima/agi_evolution/runtime/reality_state.json")

def plan():
    data=json.loads(STATE.read_text())

    missing=[]

    for name,item in data["capabilities"].items():
        if item["status"]=="missing":
            missing.append(name)

    result={
        "missing":missing,
        "priority":missing[:5],
        "action":"build_missing_capabilities"
    }

    Path(".ima/agi_evolution/runtime/upgrade_plan.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)
    )

    return result


if __name__=="__main__":
    print(json.dumps(plan(),indent=2,ensure_ascii=False))
