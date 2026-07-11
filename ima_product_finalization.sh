#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA PRODUCT FINALIZATION ==="

ROOT=$(pwd)

mkdir -p .ima/governance
mkdir -p product
mkdir -p product/childcare
mkdir -p product/adult_assistant
mkdir -p product/device_bridge
mkdir -p product/safety
mkdir -p product/voice


python3 - <<'PY'
from pathlib import Path
import json,time,importlib

report={
"time":time.time(),
"system":"IMA",
"checks":{},
"created":[],
"errors":[],
"connections":[]
}

# brain
brain=Path("learning/meta_orchestrator.py")
if brain.exists():
    report["checks"]["brain"]="OK"
else:
    report["errors"].append("missing brain")


# orchestrator
orch=Path("learning/module_registry.py")
if orch.exists():
    report["checks"]["orchestrator"]="OK"
else:
    report["errors"].append("missing orchestrator")


modules=[
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

loaded=0

for m in modules:
    try:
        importlib.import_module("learning."+m)
        loaded+=1
    except Exception as e:
        report["errors"].append(
            {"module":m,"error":str(e)}
        )

report["checks"]["learning_modules"]=loaded


files={
"product/childcare/ima_child_companion.json":{
"role":"global_child_companion",
"features":[
"learning",
"safety",
"education",
"emotional_support"
]
},

"product/adult_assistant/ima_adult_companion.json":{
"role":"life_assistant",
"features":[
"planning",
"knowledge",
"support"
]
},

"product/device_bridge/device_protocol.json":{
"targets":[
"mobile",
"robot",
"iot",
"future_devices"
]
},

"product/safety/safety_policy.json":{
"principles":[
"child_safety",
"privacy",
"human_control",
"transparent_ai"
]
},

"product/voice/voice_pipeline.json":{
"status":"foundation",
"input":"speech",
"output":"voice"
}

}

for f,data in files.items():
    p=Path(f)
    if not p.exists():
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(
            json.dumps(data,indent=2,ensure_ascii=False),
            encoding="utf8"
        )
        report["created"].append(f)


registry={
"system":"IMA",
"brain":"learning/meta_orchestrator.py",
"orchestrator":"learning/module_registry.py",
"runtime_policy":"single_runtime_only",
"duplicate_creation":"blocked",
"product_ready_layer":True
}

Path(".ima/governance/FINAL_PRODUCT_REGISTRY.json").write_text(
json.dumps(registry,indent=2,ensure_ascii=False),
encoding="utf8"
)

report["checks"]["product_registry"]="CREATED"

Path(".ima/governance/FINAL_PRODUCTIZATION_REPORT.json").write_text(
json.dumps(report,indent=2,ensure_ascii=False),
encoding="utf8"
)

print(json.dumps(report,indent=2,ensure_ascii=False))

PY


echo
echo "=== FULL CHECK ==="

python3 learning/module_registry.py
python3 ima_full_system_check.py

echo
echo "=== FILES ==="

ls -la .ima/governance/FINAL_PRODUCT_REGISTRY.json
ls -la .ima/governance/FINAL_PRODUCTIZATION_REPORT.json

echo
echo "=== GIT ==="

git status

echo
echo "=== DONE ==="
