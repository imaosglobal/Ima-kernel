from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

def check():
    checks={}

    files=[
        "system_state.json",
        "module_registry.json",
        "latest_cycle.json"
    ]

    for f in files:
        checks[f]= (ROOT/f).exists()

    state={
        "time":time.time(),
        "healthy":all(checks.values()),
        "checks":checks
    }

    (ROOT/"health_state.json").write_text(
        json.dumps(state,indent=2)
    )

    return state


if __name__=="__main__":
    print(json.dumps(check(),indent=2))
