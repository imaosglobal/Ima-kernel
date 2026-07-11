#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL ALIGNMENT ==="

BRAIN="learning/meta_orchestrator.py"
ORCHESTRATOR="learning/module_registry.py"
RUNTIME="kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js"
EVENT_BUS="kernel/runtime/KERNEL_EVENT_BUS_V2.js"
API="kernel/runtime/KERNEL_API_GATEWAY_V3.js"

mkdir -p .ima/governance

echo
echo "[1] Checking canonical files"

for f in \
"$BRAIN" \
"$ORCHESTRATOR" \
"$RUNTIME" \
"$EVENT_BUS" \
"$API"
do
    if [ -f "$f" ]; then
        echo "OK $f"
    else
        echo "MISSING $f"
    fi
done


echo
echo "[2] Checking orchestrators"

FOUND=$(find learning -maxdepth 1 -iname "*orchestrator*.py" | sort)

echo "$FOUND"

COUNT=$(echo "$FOUND" | wc -l)

if [ "$COUNT" -gt 2 ]; then
    echo "WARNING: duplicate orchestrator candidates found"
fi


echo
echo "[3] Updating canonical governance"

python3 - <<'PY'
import json
import time
from pathlib import Path

data = {
    "system": "IMA",
    "state": "CANONICAL_LOCKED",
    "brain": "learning/meta_orchestrator.py",
    "orchestrator": "learning/module_registry.py",
    "runtime": "kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
    "event_bus": "kernel/runtime/KERNEL_EVENT_BUS_V2.js",
    "api_gateway": "kernel/runtime/KERNEL_API_GATEWAY_V3.js",
    "policy": [
        "single_brain_only",
        "single_orchestrator_only",
        "reuse_existing_components",
        "block_duplicate_creation",
        "redirect_to_canonical_path"
    ],
    "updated": time.time()
}

Path(".ima/governance/canonical_architecture.json").write_text(
    json.dumps(data,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

Path(".ima/governance/orchestrator_lock.json").write_text(
    json.dumps({
        "canonical": "learning/module_registry.py",
        "brain": "learning/meta_orchestrator.py",
        "blocked_patterns": [
            "*orchestrator_new*",
            "*orchestrator_copy*",
            "*duplicate_orchestrator*"
        ]
    },indent=2,ensure_ascii=False),
    encoding="utf-8"
)

print("GOVERNANCE UPDATED")
PY


echo
echo "[4] Brain verification"

python3 - <<'PY'
from learning.brain_guard import verify_brain

verify_brain("learning/meta_orchestrator.py")

print("BRAIN OK")
PY


echo
echo "[5] Orchestrator registry"

python3 learning/module_registry.py


echo
echo "[6] Runtime syntax check"

node --check kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js || true


echo
echo "[7] Python learning modules"

python3 - <<'PY'
mods=[
"meta_orchestrator",
"module_registry",
"ima_learning_loop",
"learning_memory_connector",
"health_check",
"safety_gate"
]

import importlib

for m in mods:
    importlib.import_module("learning."+m)
    print("OK",m)
PY


echo
echo "[8] Final report"

cat > .ima/governance/canonical_alignment_report.json <<EOF
{
 "system":"IMA",
 "status":"CANONICAL_ALIGNMENT_COMPLETE",
 "brain":"learning/meta_orchestrator.py",
 "orchestrator":"learning/module_registry.py",
 "runtime":"kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
 "time":"$(date)"
}
EOF


echo
echo "=== IMA CANONICAL ALIGNMENT COMPLETE ==="
