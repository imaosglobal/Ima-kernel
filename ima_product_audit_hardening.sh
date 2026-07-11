#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA PRODUCT AUDIT HARDENING ==="

mkdir -p .ima/governance

python3 - <<'PY'
from pathlib import Path
import json
import time
import importlib

report = {
    "time": time.time(),
    "system": "IMA",
    "checks": {},
    "missing": [],
    "warnings": [],
    "connections": []
}

# Brain
brain = Path("learning/meta_orchestrator.py")

if brain.exists():
    report["checks"]["brain"] = "OK"
    report["connections"].append(
        "brain -> learning/meta_orchestrator.py"
    )
else:
    report["missing"].append(str(brain))


# Connector
connector = Path("learning/connect_orchestrator.py")

if connector.exists():
    report["checks"]["orchestrator_connector"] = "OK"
else:
    report["missing"].append(str(connector))


# Duplicate orchestrator scan
orchestrators = list(Path("learning").glob("*orchestrator*.py"))

report["checks"]["orchestrator_files"] = [
    str(x) for x in orchestrators
]

if len(orchestrators) > 2:
    report["warnings"].append(
        "possible duplicate orchestrators"
    )


# Brain guard
try:
    from learning.brain_guard import verify_brain
    verify_brain("learning/meta_orchestrator.py")
    report["checks"]["brain_guard"] = "OK"
except Exception as e:
    report["warnings"].append(
        "brain_guard: " + str(e)
    )


# Modules
modules = [
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

loaded=[]

for m in modules:
    try:
        importlib.import_module("learning."+m)
        loaded.append(m)
    except Exception as e:
        report["missing"].append(
            {"module":m,"error":str(e)}
        )

report["checks"]["learning_modules_loaded"] = len(loaded)


# Runtime
runtime_paths=[
"kernel/runtime",
"ima_product_runtime.py",
"kernel/runtime/IMA_PRODUCT_GATEWAY.js",
"kernel/runtime/KERNEL_API_GATEWAY.js"
]

for p in runtime_paths:
    if Path(p).exists():
        report["checks"][p]="EXISTS"
    else:
        report["missing"].append(p)


# Devices
device_paths=[
"devices",
"product/device_bridge",
"device_manager.py"
]

for p in device_paths:
    if Path(p).exists():
        report["checks"][p]="EXISTS"
    else:
        report["missing"].append(p)


# Product registry
registry = Path(
".ima/governance/PRODUCT_FINAL_AUDIT_REGISTRY.json"
)

data={
"system":"IMA",
"state":"AUDITED",
"brain":"learning/meta_orchestrator.py",
"connector":"learning/connect_orchestrator.py",
"policy":[
"single_brain_only",
"single_orchestrator_only",
"no_duplicate_creation",
"future_changes_require_gate"
],
"time":time.time()
}

registry.write_text(
json.dumps(
data,
indent=2,
ensure_ascii=False
),
encoding="utf-8"
)

report["registry"]=str(registry)

Path(
".ima/governance/PRODUCT_FINAL_AUDIT_REPORT.json"
).write_text(
json.dumps(
report,
indent=2,
ensure_ascii=False
),
encoding="utf-8"
)

print(json.dumps(
report,
indent=2,
ensure_ascii=False
))

PY

echo
echo "=== GOVERNANCE FILES ==="

ls -la .ima/governance/PRODUCT_FINAL_AUDIT*

echo
echo "=== GIT STATUS ==="

git status

echo
echo "=== COMPLETE ==="
