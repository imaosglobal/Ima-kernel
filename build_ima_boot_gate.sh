#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE="$HOME/ima_kernel"
RUNTIME="$BASE/.ima/agi_evolution/runtime"

echo "[1] CREATE BOOT GATE"

cat > "$RUNTIME/ima_boot_gate.py" <<'PY'
from pathlib import Path
import json,time,subprocess,sys

ROOT=Path(".ima/agi_evolution/runtime")

def load(name):
    p=ROOT/name
    if p.exists():
        return json.loads(p.read_text())
    return {}

def boot():

    state={
        "time":time.time(),
        "boot":"active",
        "source":"ima_boot_gate",
        "runtime":load("ima_master_state.json"),
        "brain":load("brain_state.json"),
        "decision":load("decision_state.json"),
        "handoff":"kernel_ready"
    }

    (ROOT/"boot_gate_state.json").write_text(
        json.dumps(state,indent=2,ensure_ascii=False)
    )

    return state


if __name__=="__main__":
PY


echo "[2] CREATE MASTER ENTRY MAP"

python3 <<'PY'
from pathlib import Path
import json,time

root=Path(".ima/agi_evolution/runtime")

data={
"time":time.time(),
"entry":"ima_boot_gate.py",
"flow":[
"boot_gate",
"ima_master_runtime",
"brain_controller",
"decision_engine",
"kernel"
],
"status":"ready"
}

(root/"MASTER_ENTRY_MAP.json").write_text(
json.dumps(data,indent=2,ensure_ascii=False)
)
PY


echo "[3] TEST BOOT GATE"

cd "$BASE"

python3 "$RUNTIME/ima_boot_gate.py"


echo "[4] PYTHON CHECK"

python3 -m py_compile \
"$RUNTIME/ima_boot_gate.py"


echo "[5] ADD CRON HANDOFF"

(crontab -l 2>/dev/null | grep -v "ima_boot_gate.py"; \
echo "*/30 * * * * cd $BASE && python3 .ima/agi_evolution/runtime/ima_boot_gate.py >> $RUNTIME/boot_gate.log 2>&1") | crontab -


echo "[6] GIT SAVE"

git add .
git commit -m "IMA boot gate single entry layer" || true
git push || true


echo "=== IMA BOOT GATE READY ==="

