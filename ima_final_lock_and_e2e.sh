#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA FINAL CANONICAL BUILD ==="

mkdir -p .ima/governance

echo "[1] Checking canonical brain"

BRAIN="learning/meta_orchestrator.py"

if [ -f "$BRAIN" ]; then
    echo "OK brain: $BRAIN"
else
    echo "MISSING brain"
    exit 1
fi


echo "[2] Checking orchestrator"

if [ -f "learning/module_registry.py" ]; then
    ORCH="learning/module_registry.py"
else
    echo "Creating orchestrator connector"

cat > learning/module_registry.py <<'PY'
import importlib,json,time
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
    data={
        "system":"IMA",
        "type":"canonical_orchestrator",
        "modules":[],
        "time":time.time()
    }

    for m in MODULES:
        try:
            importlib.import_module("learning."+m)
            data["modules"].append(
                {"module":m,"status":"ok"}
            )
        except Exception as e:
            data["modules"].append(
                {"module":m,"status":"error","error":str(e)}
            )

    Path(".ima/governance/orchestrator_registry.json").write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return data


if __name__=="__main__":
    build_registry()
PY

    ORCH="learning/module_registry.py"
fi


echo "[3] Selecting runtime"

if [ -f kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js ]; then
    RUNTIME="kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js"
elif [ -f kernel/runtime/SYSTEM_KERNEL_STABLE_SINGLESHOT_V1.js ]; then
    RUNTIME="kernel/runtime/SYSTEM_KERNEL_STABLE_SINGLESHOT_V1.js"
else
    echo "No runtime found"
    exit 1
fi


echo "[4] Selecting event bus"

if [ -f kernel/runtime/KERNEL_EVENT_BUS_V2.js ]; then
    EVENT="kernel/runtime/KERNEL_EVENT_BUS_V2.js"
elif [ -f kernel/runtime/KERNEL_EVENT_BUS.js ]; then
    EVENT="kernel/runtime/KERNEL_EVENT_BUS.js"
else
    echo "Missing event bus"
    exit 1
fi


echo "[5] Selecting API"

if [ -f kernel/runtime/KERNEL_API_GATEWAY_V3.js ]; then
    API="kernel/runtime/KERNEL_API_GATEWAY_V3.js"
elif [ -f kernel/runtime/KERNEL_API_GATEWAY.js ]; then
    API="kernel/runtime/KERNEL_API_GATEWAY.js"
else
    echo "Missing API gateway"
    exit 1
fi


echo "[6] Creating canonical map"

cat > .ima/governance/CANONICAL_MAP.json <<EOF
{
 "system":"IMA",
 "state":"LOCKED",
 "brain":"$BRAIN",
 "orchestrator":"$ORCH",
 "runtime":"$RUNTIME",
 "event_bus":"$EVENT",
 "api_gateway":"$API",
 "policies":[
   "single_brain_only",
   "single_orchestrator_only",
   "reuse_existing_components",
   "block_duplicate_creation"
 ],
 "timestamp":"$(date -Iseconds)"
}
EOF


echo "[7] Duplicate creation guard"

cat > learning/canonical_guard.py <<'PY'
from pathlib import Path
import json

CANONICAL=json.loads(
Path(".ima/governance/CANONICAL_MAP.json").read_text()
)

def check(path):

    forbidden=[
        "new_brain",
        "new_orchestrator",
        "another_kernel"
    ]

    for x in forbidden:
        if x in path.lower():
            raise RuntimeError(
f"""
IMA BLOCKED DUPLICATE

Use existing canonical:
{CANONICAL}
"""
)

    return True
PY


echo "[8] Running Python checks"

python3 -m py_compile \
learning/meta_orchestrator.py \
learning/module_registry.py \
learning/canonical_guard.py


echo "[9] Running orchestrator"

python3 learning/module_registry.py || true


echo "[10] Running system checks"

if [ -f ima_full_system_check.py ]; then
    python3 ima_full_system_check.py
fi


echo "[11] Git freeze"

git add .ima/governance learning/canonical_guard.py learning/module_registry.py

git commit -m "IMA canonical brain runtime e2e lock" || true

git tag -a IMA_TRUE_CANONICAL_SYSTEM_LOCKED_v1 \
-m "IMA single brain complete architecture lock" || true


echo ""
echo "================================"
echo "IMA FINAL LOCK COMPLETE"
echo "Brain: $BRAIN"
echo "Orchestrator: $ORCH"
echo "Runtime: $RUNTIME"
echo "Event: $EVENT"
echo "API: $API"
echo "================================"

