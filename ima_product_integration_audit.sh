#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

REPORT=".ima/governance/product_integration_final_report.json"

echo "=== IMA PRODUCT INTEGRATION ==="

mkdir -p .ima/governance

python3 - <<'PY'
from pathlib import Path
import json, time, importlib

root = Path(".")
gov = root / ".ima/governance"

report = {
    "time": time.time(),
    "system": "IMA",
    "checks": {},
    "created": [],
    "missing": [],
    "connections": [],
    "status": ""
}

# Canonical brain
brain = Path("learning/meta_orchestrator.py")
if brain.exists():
    report["checks"]["brain"] = "OK"
    report["connections"].append(
        "brain -> learning/meta_orchestrator.py"
    )
else:
    report["checks"]["brain"] = "MISSING"
    report["missing"].append(str(brain))

# Orchestrator
orch = Path("learning/connect_orchestrator.py")
if orch.exists():
    report["checks"]["orchestrator_connector"] = "OK"
else:
    report["missing"].append(str(orch))

# Learning modules
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

loaded = []

for m in modules:
    try:
        importlib.import_module("learning." + m)
        loaded.append(m)
    except Exception as e:
        report["missing"].append(
            {"module":m,"error":str(e)}
        )

report["checks"]["learning_modules_loaded"] = len(loaded)
report["connections"].append(
    f"learning orchestrator connected modules: {len(loaded)}"
)

# Product layers
layers = {
    "android":"android",
    "web":"ima-ui",
    "api":"kernel/runtime",
    "devices":"devices",
    "voice":".ima/voice.json",
    "memory":".ima/memory.json",
    "safety":".ima/governance"
}

for name,path in layers.items():
    if Path(path).exists():
        report["checks"][name]="EXISTS"
    else:
        report["missing"].append(path)

# Create missing governance manifests only
registries = {
    ".ima/governance/product_runtime_registry.json": {
        "system":"IMA",
        "brain":"learning/meta_orchestrator.py",
        "orchestrator":"learning/meta_orchestrator.py",
        "stage":"product_integration"
    },
    ".ima/governance/device_layer_registry.json": {
        "devices":"partial",
        "next":"device abstraction layer"
    },
    ".ima/governance/safety_product_registry.json": {
        "required":True,
        "stage":"design"
    }
}

for file,data in registries.items():
    p=Path(file)
    if not p.exists():
        p.write_text(
            json.dumps(data,indent=2,ensure_ascii=False),
            encoding="utf-8"
        )
        report["created"].append(file)

report["status"]="completed"

Path(".ima/governance/product_integration_final_report.json").write_text(
    json.dumps(report,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

print(json.dumps(report,indent=2,ensure_ascii=False))
PY

echo
echo "=== GIT STATE ==="
git status --short

echo
echo "=== REPORT ==="
cat "$REPORT"

echo
echo "=== COMPLETE ==="
