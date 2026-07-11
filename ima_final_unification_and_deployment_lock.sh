#!/data/data/com.termux/files/usr/bin/bash
set -e

cd "$HOME/ima_kernel"

echo "=== IMA FINAL UNIFICATION AND DEPLOYMENT LOCK ==="

mkdir -p .ima/governance

echo
echo "[1] Checking canonical brain and orchestrators"

python3 - <<'PY'
from pathlib import Path

files=[
"learning/meta_orchestrator.py",
"learning/connect_orchestrator.py",
"learning/ima_learning_loop.py",
"learning/safety_gate.py",
"learning/child_safety_engine.py"
]

for f in files:
    if Path(f).exists():
        print("OK",f)
    else:
        print("MISSING",f)
PY


echo
echo "[2] Orchestrator consolidation"

python3 - <<'PY'
import json
from pathlib import Path

registry={
"system":"IMA",
"orchestrator":"learning/connect_orchestrator.py",
"brain":"learning/meta_orchestrator.py",
"active_orchestrators":[
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
],
"policy":"single_orchestrator_only"
}

Path(".ima/governance/final_orchestrator_lock.json").write_text(
json.dumps(registry,indent=2)
)

print("ORCHESTRATOR LOCKED")
PY


echo
echo "[3] Creating deployment layer"

cat > kernel/runtime/IMA_DEPLOYMENT_CORE_V1.js <<'JS'
class IMA_DEPLOYMENT_CORE_V1 {

constructor(){
this.name="IMA_DEPLOYMENT_CORE_V1";
this.status="active";
}

health(){
return {
deployment:this.name,
status:this.status
};
}

}

module.exports=IMA_DEPLOYMENT_CORE_V1;
JS


echo "DEPLOYMENT CORE CREATED"


echo
echo "[4] Runtime chain verification"

node - <<'JS'
const Runtime=require("./kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1");
const Bus=require("./kernel/runtime/KERNEL_EVENT_BUS_V2");
const Api=require("./kernel/runtime/KERNEL_API_GATEWAY_V3");
const Service=require("./kernel/runtime/IMA_SERVICE_CORE_V1");
const Deploy=require("./kernel/runtime/IMA_DEPLOYMENT_CORE_V1");

console.log("RUNTIME OK");
console.log(new Service().health());
console.log(new Deploy().health());
JS


echo
echo "[5] Duplicate detection"

python3 - <<'PY'
from pathlib import Path
from collections import defaultdict

targets=[
"SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
"KERNEL_EVENT_BUS_V2.js",
"KERNEL_API_GATEWAY_V3.js",
"IMA_SERVICE_CORE_V1.js",
"meta_orchestrator.py",
"connect_orchestrator.py"
]

for t in targets:
    found=list(Path(".").rglob(t))
    print("\n",t)
    print("COUNT:",len(found))
    for x in found[:5]:
        print(x)
PY


echo
echo "[6] Final canonical state"

python3 - <<'PY'
import json,time
from pathlib import Path

state={
"system":"IMA",
"status":"FINAL_CANONICAL_LOCKED",
"brain":"learning/meta_orchestrator.py",
"orchestrator":"learning/connect_orchestrator.py",
"runtime":"kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
"event_bus":"kernel/runtime/KERNEL_EVENT_BUS_V2.js",
"api":"kernel/runtime/KERNEL_API_GATEWAY_V3.js",
"service":"kernel/runtime/IMA_SERVICE_CORE_V1.js",
"deployment":"kernel/runtime/IMA_DEPLOYMENT_CORE_V1.js",
"policies":[
"single_brain",
"single_orchestrator",
"single_runtime",
"reuse_existing_components",
"block_duplicate_creation"
],
"time":time.time()
}

Path(".ima/governance/FINAL_CANONICAL_STATE.json").write_text(
json.dumps(state,indent=2)
)

print("FINAL STATE SAVED")
PY


echo
echo "=== IMA FINAL UNIFICATION COMPLETE ==="

