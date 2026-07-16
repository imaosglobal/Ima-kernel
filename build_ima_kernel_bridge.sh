#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE="$HOME/ima_kernel"
RUNTIME="$BASE/.ima/agi_evolution/runtime"
BACKUP="$BASE/.ima/backups/kernel_bridge_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP"
mkdir -p "$RUNTIME"

echo "[1] BACKUP CORE FILES"

find "$BASE" \
\( -name "kernel.py" -o -name "MOTHER_ENTRY.py" -o -name "mother*.py" \) \
-type f \
| while read f; do
    cp "$f" "$BACKUP"/
done || true


echo "[2] SCAN ENTRY POINTS"

find "$BASE" \
\( -name "kernel.py" -o -name "MOTHER_ENTRY.py" -o -name "mother*.py" \) \
-type f \
> "$RUNTIME/kernel_entry_scan.txt"


grep -R "def run\|def boot\|if __name__" \
"$BASE/ima" "$BASE/.ima" \
2>/dev/null \
> "$RUNTIME/kernel_functions_scan.txt" || true


echo "[3] CREATE AGI BRIDGE"

cat > "$RUNTIME/ima_agi_bridge.py" <<'PY'
from pathlib import Path
import json,time,subprocess,sys

ROOT=Path(".ima/agi_evolution/runtime")

def start_agi_layer():

    result={
        "time":time.time(),
        "status":"started",
        "layers":[]
    }

    jobs=[
        "ima_master_runtime.py",
        "decision_engine.py",
        "brain_controller.py"
    ]

    for job in jobs:
        try:
            out=subprocess.check_output(
                [sys.executable,str(ROOT/job)],
                text=True
            )

            result["layers"].append({
                "job":job,
                "status":"ok",
                "output":out[-200:]
            })

        except Exception as e:
            result["layers"].append({
                "job":job,
                "status":"failed",
                "error":str(e)
            })

    (ROOT/"agi_bridge_state.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)
    )

    return result


if __name__=="__main__":
    print(start_agi_layer())
PY


echo "[4] CREATE MASTER REGISTRY"

python3 <<'PY'
from pathlib import Path
import json,time

root=Path(".ima/agi_evolution/runtime")

registry={
"time":time.time(),
"status":"active",
"components":[
"brain_controller",
"ima_master_runtime",
"decision_engine",
"lifecycle",
"future_planner",
"memory_consolidator"
],
"next":"kernel_bridge"
}

(root/"IMA_MASTER_REGISTRY.json").write_text(
json.dumps(registry,indent=2,ensure_ascii=False)
)
PY


echo "[5] RUN TEST"

cd "$BASE"

python3 "$RUNTIME/ima_agi_bridge.py"

python3 -m py_compile \
"$RUNTIME/ima_agi_bridge.py" \
"$RUNTIME/ima_master_runtime.py" \
"$RUNTIME/decision_engine.py" \
"$RUNTIME/brain_controller.py"


echo "[6] RUN LIFECYCLE"

python3 "$RUNTIME/ima_lifecycle.py" || true


echo "[7] UPDATE CRON"

(crontab -l 2>/dev/null | grep -v "ima_agi_bridge.py"; \
echo "*/15 * * * * cd $BASE && python3 .ima/agi_evolution/runtime/ima_agi_bridge.py >> $RUNTIME/agi_bridge.log 2>&1") | crontab -


echo "[8] GIT CHECKPOINT"

git add .
git commit -m "IMA kernel bridge integration" || true
git push || true


echo "=== IMA KERNEL BRIDGE READY ==="
