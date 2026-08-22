#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA PRODUCT EVOLUTION ==="

ROOT=$(pwd)
mkdir -p .ima/governance

REPORT=".ima/governance/product_evolution_report.json"

python3 - <<'PY'
from pathlib import Path
import json, time, hashlib

checks = {}

targets = {
    "product_runtime": [
        "product/runtime",
        "kernel/runtime",
        "ima_product_runtime.py"
    ],
    "identity": [
        "product/identity",
        "identity",
        "user_identity.py"
    ],
    "safety": [
        "product/safety",
        ".ima/governance/safety_product_registry.json"
    ],
    "device_bridge": [
        "product/device_bridge",
        "devices",
        "device"
    ],
    "gateway": [
        "kernel/runtime/IMA_PRODUCT_GATEWAY.js",
        "kernel/runtime/KERNEL_API_GATEWAY.js"
    ]
}

for name, paths in targets.items():
    found=[p for p in paths if Path(p).exists()]
    checks[name]={
        "exists": bool(found),
        "found": found
    }

created=[]

# Create only missing product manifests
files={
"product/runtime/product_runtime_registry.json":{
"system":"IMA",
"brain":"learning/meta_orchestrator.py",
"policy":"single_runtime_only"
},
"product/identity/identity_registry.json":{
"system":"IMA",
"type":"identity_layer",
"status":"foundation"
},
"product/safety/safety_runtime_registry.json":{
"system":"IMA",
"type":"safety_runtime",
"status":"foundation"
}
}

for f,data in files.items():
    p=Path(f)
    if not p.exists():
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(
            json.dumps(data,indent=2,ensure_ascii=False),
            encoding="utf-8"
        )
        created.append(f)

lock={
"system":"IMA",
"state":"PRODUCT_EVOLUTION_LOCKED",
"brain":"learning/meta_orchestrator.py",
"orchestrator":"learning/module_registry.py",
"duplicate_creation":"blocked",
"created":created,
"time":time.time()
}

Path(".ima/governance/PRODUCT_EVOLUTION_LOCK.json").write_text(
    json.dumps(lock,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

report={
"system":"IMA",
"checks":checks,
"created":created,
"lock":"PRODUCT_EVOLUTION_LOCK.json",
"status":"completed"
}

Path(".ima/governance/product_evolution_report.json").write_text(
    json.dumps(report,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

PY

echo
echo "=== RUN CONNECTIVITY ==="
python3 learning/module_registry.py
python3 ima_full_system_check.py

echo
echo "=== FILES ==="
ls -la .ima/governance/PRODUCT_EVOLUTION_LOCK.json
ls -la .ima/governance/product_evolution_report.json

echo
echo "=== GIT ==="
git status

echo
echo "=== DONE ==="
