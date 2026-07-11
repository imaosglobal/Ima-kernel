#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA CANONICAL FINALIZATION ==="

mkdir -p .ima/governance

echo "[1] Creating active architecture registry"

python3 - <<'PY'
from pathlib import Path
import json,time

state={
    "system":"IMA",
    "state":"CANONICAL_LOCKED",
    "active":{
        "brain":"learning/meta_orchestrator.py",
        "connector":"learning/connect_orchestrator.py",
        "runtime":"kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
        "event_bus":"kernel/runtime/KERNEL_EVENT_BUS_V2.js",
        "api":"kernel/runtime/KERNEL_API_GATEWAY_V3.js",
        "service":"kernel/runtime/IMA_SERVICE_CORE_V1.js"
    },
    "snapshots":{
        "allowed":True,
        "runtime_loading":False,
        "path":".ima/snapshots/"
    },
    "policies":[
        "single_brain_only",
        "single_connector_only",
        "single_runtime_only",
        "no_duplicate_active_modules",
        "snapshots_are_read_only_history"
    ],
    "locked_at":time.time()
}

Path(".ima/governance/ACTIVE_ARCHITECTURE.json").write_text(
    json.dumps(state,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

print("ACTIVE ARCHITECTURE SAVED")
PY


echo "[2] Checking canonical files"

python3 - <<'PY'
from pathlib import Path

files=[
"learning/meta_orchestrator.py",
"learning/connect_orchestrator.py",
"kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
"kernel/runtime/KERNEL_EVENT_BUS_V2.js",
"kernel/runtime/KERNEL_API_GATEWAY_V3.js",
"kernel/runtime/IMA_SERVICE_CORE_V1.js"
]

for f in files:
    p=Path(f)
    print(f, "OK" if p.exists() else "MISSING")
PY


echo "[3] Checking duplicates excluding snapshots"

python3 - <<'PY'
from pathlib import Path

targets=[
"meta_orchestrator.py",
"connect_orchestrator.py",
"SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
"KERNEL_EVENT_BUS_V2.js",
"KERNEL_API_GATEWAY_V3.js",
"IMA_SERVICE_CORE_V1.js"
]

for t in targets:
    active=[
        x for x in Path(".").rglob(t)
        if ".ima/snapshots" not in str(x)
    ]
    print(t, "ACTIVE COPIES:", len(active))
    for x in active:
        print(" ",x)
PY


echo "[4] Runtime verification"

python3 ima_full_system_check.py


echo "[5] Brain verification"

python3 - <<'PY'
from learning.brain_guard import verify_brain
verify_brain("learning/meta_orchestrator.py")
print("BRAIN LOCK OK")
PY


echo "[6] Git finalize"

git add .ima/governance/ACTIVE_ARCHITECTURE.json

git commit -m "IMA canonical active architecture locked" || true

git tag -a IMA_CANONICAL_ACTIVE_STATE_v1 \
-m "IMA single active brain runtime architecture locked" || true


echo "=== IMA CANONICAL LOCK COMPLETE ==="
