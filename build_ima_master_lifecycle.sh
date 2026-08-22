#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel/.ima/agi_evolution/runtime"

mkdir -p "$ROOT"

echo "[1] CONNECT BRAIN TO MASTER RUNTIME"

cat > "$ROOT/ima_master_runtime.py" <<'PY'
from pathlib import Path
import json,time,subprocess,sys

ROOT=Path(".ima/agi_evolution/runtime")

def load(name):
    p=ROOT/name
    if p.exists():
        return json.loads(p.read_text())
    return {}

def run():

    state={
        "time":time.time(),
        "runtime":"active",
        "brain":load("brain_state.json"),
        "health":load("health_state.json"),
        "supervisor":load("supervisor_state.json"),
        "decision":"continue"
    }

    if state["health"].get("healthy") is False:
        state["decision"]="repair"

    (ROOT/"ima_master_state.json").write_text(
        json.dumps(state,indent=2,ensure_ascii=False)
    )

    return state


if __name__=="__main__":
PY


echo "[2] DECISION ENGINE"

cat > "$ROOT/decision_engine.py" <<'PY'
from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

def decide():

    master=json.loads(
        (ROOT/"ima_master_state.json").read_text()
    )

    decision={
        "time":time.time(),
        "current":master.get("decision"),
        "next_action":"continue_evolution_cycle",
        "priority":"stability"
    }

    (ROOT/"decision_state.json").write_text(
        json.dumps(decision,indent=2,ensure_ascii=False)
    )

    return decision


if __name__=="__main__":
PY


echo "[3] LIFECYCLE"

cat > "$ROOT/ima_lifecycle.py" <<'PY'
import subprocess,sys,json,time
from pathlib import Path

ROOT=Path(".ima/agi_evolution/runtime")

JOBS=[
"ima_master_runtime.py",
"decision_engine.py",
"brain_controller.py"
]

def run():

    result={
        "time":time.time(),
        "cycle":"started",
        "steps":[]
    }

    for j in JOBS:
        try:
            out=subprocess.check_output(
                [sys.executable,str(ROOT/j)],
                text=True
            )

            result["steps"].append({
                "job":j,
                "status":"ok",
                "output":out[-300:]
            })

        except Exception as e:
            result["steps"].append({
                "job":j,
                "status":"failed",
                "error":str(e)
            })

    (ROOT/"lifecycle_state.json").write_text(
        json.dumps(result,indent=2)
    )

    return result


if __name__=="__main__":
PY


echo "[4] PLANNING SYSTEM"

cat > "$ROOT/future_planner.py" <<'PY'
from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

plan={
"time":time.time(),
"daily":{
"goal":"maintain and improve runtime"
},
"weekly":{
"goal":"validate and expand modules"
},
"monthly":{
"goal":"increase integration"
},
"yearly":{
"goal":"build mature ecosystem"
},
"eternal":{
"goal":"continuous evolution with memory"
}
}

(ROOT/"future_plan.json").write_text(
json.dumps(plan,indent=2,ensure_ascii=False)
)

PY


echo "[5] MEMORY CONSOLIDATION"

cat > "$ROOT/memory_consolidator.py" <<'PY'
from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

files=[
"evolution_history.json",
"brain_state.json",
"supervisor_state.json",
"decision_state.json"
]

memory={
"time":time.time(),
"sources":{}
}

for f in files:
    p=ROOT/f
    if p.exists():
        memory["sources"][f]=json.loads(p.read_text())

(ROOT/"ima_long_term_memory.json").write_text(
json.dumps(memory,indent=2,ensure_ascii=False)
)

PY


echo "[6] RUN MASTER"

cd "$HOME/ima_kernel"

python3 .ima/agi_evolution/runtime/ima_lifecycle.py
python3 .ima/agi_evolution/runtime/future_planner.py
python3 .ima/agi_evolution/runtime/memory_consolidator.py


echo "[7] GIT CHECKPOINT"

git add .
git commit -m "IMA master lifecycle integration" || true
git push || true


echo "[8] MASTER CRON"

(crontab -l 2>/dev/null | grep -v "ima_lifecycle.py"; \
echo "0 6 * * * cd $HOME/ima_kernel && python3 .ima/agi_evolution/runtime/ima_lifecycle.py >> $HOME/ima_kernel/.ima/agi_evolution/runtime/master.log 2>&1") | crontab -


echo "=== IMA MASTER LIFECYCLE READY ==="

