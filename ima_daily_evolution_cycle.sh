#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA DAILY EVOLUTION CYCLE ==="

NOW=$(date +%Y-%m-%d_%H-%M-%S)

mkdir -p \
.ima/agi_evolution/runtime/history \
.ima/agi_evolution/plans \
.ima/agi_evolution/backups


echo "[1] SYSTEM SNAPSHOT"

python3 - <<'PY'
from pathlib import Path
import json,time

root=Path(".")
files=list(root.rglob("*"))

state={
"time":time.time(),
"files":len(files),
"python_files":len(list(root.rglob("*.py"))),
"status":"alive"
}

Path(".ima/agi_evolution/runtime/system_state.json").write_text(
json.dumps(state,indent=2)
)

PY


echo "[2] MODULE DISCOVERY"

python3 .ima/agi_evolution/runtime/integration_engine.py \
> .ima/agi_evolution/runtime/module_scan.json || true


echo "[3] AUTONOMOUS PLAN"

python3 .ima/agi_evolution/runtime/autonomous_evolution_controller.py \
> .ima/agi_evolution/runtime/latest_cycle.json || true


echo "[4] CREATE TIME PLANS"

python3 - <<'PY'
from pathlib import Path
import json,time

base=Path(".ima/agi_evolution/plans")

plans={
"daily":{
"focus":["health_check","tests","bug_fix","learning"]
},
"weekly":{
"focus":["architecture","integration","optimization"]
},
"monthly":{
"focus":["new_capabilities","performance","security"]
},
"yearly":{
"focus":["vision","product","global_growth"]
},
"future":{
"focus":["continuous_improvement","knowledge_expansion"]
},
"time":time.time()
}

for k,v in plans.items():
    (base/f"{k}.json").write_text(
        json.dumps(v,indent=2,ensure_ascii=False)
    )

PY


echo "[5] BACKUP"

tar -czf \
".ima/agi_evolution/backups/ima_$NOW.tar.gz" \
.ima \
ima_master_runtime.py \
IMA_START.py \
2>/dev/null || true


echo "[6] GIT SYNC"

if [ -d ".git" ]; then

git add . || true

git commit \
-m "IMA autonomous evolution checkpoint $NOW" \
|| true

git push || true

echo "git sync attempted"

else

echo "no git repository"

fi


echo "[7] SAVE MEMORY"

python3 - <<'PY'
from pathlib import Path
import json,time

p=Path(".ima/agi_evolution/runtime/evolution_memory.json")

data=[]

if p.exists():
    data=json.loads(p.read_text())

data.append({
"time":time.time(),
"event":"daily evolution cycle completed",
"status":"alive"
})

p.write_text(
json.dumps(data,indent=2)
)

PY


echo "=== IMA READY FOR NEXT CYCLE ==="
