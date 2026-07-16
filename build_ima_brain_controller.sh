#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel/.ima/agi_evolution/runtime"

mkdir -p "$ROOT"

echo "[1] CONTINUITY ENGINE"

cat > "$ROOT/continuity_engine.py" <<'PY'
from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")
STATE=ROOT/"continuity_state.json"

def update(event="cycle_check"):

    data={
        "time":time.time(),
        "event":event,
        "current_state":"running",
        "next_state":"continue",
        "handoff_ready":True
    }

    STATE.write_text(
        json.dumps(data,indent=2,ensure_ascii=False)
    )

    return data


if __name__=="__main__":
    print(json.dumps(update(),indent=2))
PY


echo "[2] REPAIR ENGINE"

cat > "$ROOT/repair_engine.py" <<'PY'
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
PY


echo "[3] GOAL ENGINE"

cat > "$ROOT/goal_engine.py" <<'PY'
from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

def create_goal():

    goals=[
        "maintain_runtime",
        "improve_capabilities",
        "validate_modules",
        "expand_product_layer"
    ]

    data={
        "time":time.time(),
        "priority":"system_stability",
        "goals":goals,
        "next_action":goals[0]
    }

    (ROOT/"goal_state.json").write_text(
        json.dumps(data,indent=2,ensure_ascii=False)
    )

    return data


if __name__=="__main__":
    print(json.dumps(create_goal(),indent=2))
PY


echo "[4] BRAIN CONTROLLER"

cat > "$ROOT/brain_controller.py" <<'PY'
import subprocess,sys,json,time
from pathlib import Path

ROOT=Path(".ima/agi_evolution/runtime")

def run():

    jobs=[
        "continuity_engine.py",
        "repair_engine.py",
        "goal_engine.py"
    ]

    result={
        "time":time.time(),
        "steps":[]
    }

    for job in jobs:
        try:
            out=subprocess.check_output(
                [sys.executable,str(ROOT/job)],
                text=True
            )

            result["steps"].append({
                "job":job,
                "status":"ok",
                "output":out[-300:]
            })

        except Exception as e:
            result["steps"].append({
                "job":job,
                "status":"failed",
                "error":str(e)
            })

    (ROOT/"brain_state.json").write_text(
        json.dumps(result,indent=2)
    )

    return result


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
PY


echo "[5] CONNECT SUPERVISOR"

python3 "$ROOT/brain_controller.py"


echo "[6] ADD CRON"

(crontab -l 2>/dev/null | grep -v "brain_controller.py"; \
echo "*/15 * * * * cd $HOME/ima_kernel && python3 .ima/agi_evolution/runtime/brain_controller.py >> $HOME/ima_kernel/.ima/agi_evolution/runtime/brain.log 2>&1") | crontab -


echo "=== IMA BRAIN CONTROLLER READY ==="

