from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

CHECKS=[
    "continuity_state.json",
    "supervisor_state.json",
    "health_state.json"
]

def scan():

    missing=[]

    for f in CHECKS:
        if not (ROOT/f).exists():
            missing.append(f)

    result={
        "time":time.time(),
        "missing":missing,
        "repair_needed":len(missing)>0,
        "status":"clean" if not missing else "repair_required"
    }

    (ROOT/"repair_state.json").write_text(
        json.dumps(result,indent=2)
    )

    return result


if __name__=="__main__":
    print(json.dumps(scan(),indent=2))
