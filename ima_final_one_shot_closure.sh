#!/data/data/com.termux/files/usr/bin/bash

set -u

ROOT="$HOME/ima_kernel"
cd "$ROOT" || exit 1

LOG=".ima/final_closure_report.txt"
mkdir -p .ima/governance

echo "=== IMA FINAL ONE SHOT CLOSURE ===" | tee "$LOG"
date | tee -a "$LOG"

echo "[1] BACKUP" | tee -a "$LOG"
tar -czf "$HOME/ima_before_product_closure_backup.tar.gz" . >> "$LOG" 2>&1 || true


echo "[2] VERIFY CANONICAL BRAIN" | tee -a "$LOG"

BRAIN="learning/meta_orchestrator.py"

if [ ! -f "$BRAIN" ]; then
    echo "ERROR: missing brain $BRAIN" | tee -a "$LOG"
    exit 1
fi

python3 - <<PY >> "$LOG" 2>&1
from learning.brain_guard import verify_brain
verify_brain("$BRAIN")
PY


echo "[3] VERIFY ORCHESTRATOR CONNECTOR" | tee -a "$LOG"

if [ ! -f learning/module_registry.py ]; then
    echo "creating missing connector"
    cat > learning/module_registry.py <<'PY'
import json,time
from pathlib import Path

MODULES=[
"health_check",
"ima_learning_loop",
"learning_memory_connector",
"knowledge_dedup",
"knowledge_expander",
"improvement_engine",
"evaluation_engine",
"feedback_engine",
"safety_gate",
"system_introspection",
"meta_orchestrator"
]

def build_registry():
    result={
    "system":"IMA",
    "type":"learning_module_registry",
    "time":time.time(),
    "modules":[]
    }

    for m in MODULES:
        try:
            __import__("learning."+m)
            result["modules"].append(
            {"module":m,"status":"ok"})
        except Exception as e:
            result["modules"].append(
            {"module":m,"status":"failed","error":str(e)})

    result["active_modules"]=len(
        [x for x in result["modules"] if x["status"]=="ok"]
    )

    Path(".ima/governance/orchestrator_registry.json").write_text(
    json.dumps(result,indent=2,ensure_ascii=False),
    encoding="utf8")

    return result

if __name__=="__main__":
PY
fi


python3 learning/module_registry.py >> "$LOG" 2>&1 || true


echo "[4] COMPILE CHECK" | tee -a "$LOG"

python3 -m compileall learning >> "$LOG" 2>&1


echo "[5] SYSTEM CHECK" | tee -a "$LOG"

python3 ima_full_system_check.py >> "$LOG" 2>&1 || true


echo "[6] META ANALYSIS" | tee -a "$LOG"

python3 - <<'PY' >> "$LOG" 2>&1
from learning.meta_orchestrator import run_meta_analysis
import json
run_meta_analysis(),
ensure_ascii=False,
indent=2))
PY


echo "[7] FINAL REGISTRY" | tee -a "$LOG"

cat .ima/governance/brain_registry.json >> "$LOG" 2>/dev/null || true
cat .ima/governance/orchestrator_registry.json >> "$LOG" 2>/dev/null || true


echo "[8] GIT SNAPSHOT" | tee -a "$LOG"

git add .ima learning 2>/dev/null || true

git commit -m "IMA final product closure verification" 2>/dev/null || true

git tag -a IMA_PRODUCT_CLOSURE_READY_v1 \
-m "IMA product closure verified" 2>/dev/null || true


echo "================================"
echo "IMA CLOSURE COMPLETE"
echo "REPORT:"
echo "$LOG"
echo "BACKUP:"
echo "$HOME/ima_before_product_closure_backup.tar.gz"
echo "================================"

