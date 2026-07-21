#!/data/data/com.termux/files/usr/bin/bash

set -e

cd "$HOME/ima_kernel"

echo "=== IMA SERVICE LAYER LOCK AND CONNECT ==="

mkdir -p .ima/governance


echo
echo "[1] Selecting canonical components"

python3 - <<'PY'
import json
import time
from pathlib import Path


registry = {
    "system": "IMA",

    "state": "SERVICE_LAYER_LOCKED",

    "brain":
        "learning/meta_orchestrator.py",

    "orchestrator":
        "learning/module_registry.py",

    "runtime":
        "kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",

    "event_bus":
        "kernel/runtime/KERNEL_EVENT_BUS_V2.js",

    "api_gateway":
        "kernel/runtime/KERNEL_API_GATEWAY_V3.js",

    "memory":
        ".ima/runtime/memory_bus.py",

    "device_registry":
        ".ima/governance/device_registry.json",

    "service_policy": [
        "single_service_layer_only",
        "reuse_existing_api",
        "reuse_existing_memory",
        "block_duplicate_services"
    ],

    "locked_at": time.time()
}


Path(
".ima/governance/service_registry.json"
).write_text(
    json.dumps(
        registry,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)


Path(
".ima/governance/service_layer_lock.json"
).write_text(
    json.dumps(
        {
            "canonical":
            "kernel/runtime/IMA_SERVICE_CORE_V1.js",

            "blocked_patterns":[
                "*service_copy*",
                "*service_new*",
                "*service_duplicate*"
            ]
        },
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)


print("SERVICE GOVERNANCE CREATED")

PY


echo
echo "[2] Creating service core"

mkdir -p kernel/runtime

if [ ! -f kernel/runtime/IMA_SERVICE_CORE_V1.js ]; then

cat > kernel/runtime/IMA_SERVICE_CORE_V1.js <<'JS'
const BUS = require('./KERNEL_EVENT_BUS_V2');

class IMAServiceCore {

    constructor(){
        this.name="IMA_SERVICE_CORE_V1";
        this.status="active";
    }


    health(){
        return {
            service:this.name,
            status:this.status
        };
    }


    handle(event){

        if(BUS && BUS.emit){
            BUS.emit(
                "ima.service.event",
                event
            );
        }

        return {
            received:true,
            event:event
        };
    }

}


module.exports = IMAServiceCore;
JS

echo "SERVICE CORE CREATED"

else

echo "SERVICE CORE EXISTS - REUSED"

fi



echo
echo "[3] Runtime syntax"

node --check kernel/runtime/IMA_SERVICE_CORE_V1.js


echo
echo "[4] Python brain connection"

python3 - <<'PY'

from learning.brain_guard import verify_brain

verify_brain(
"learning/meta_orchestrator.py"
)

print(
"BRAIN CONNECTION OK"
)

PY



echo
echo "[5] Memory verification"

python3 - <<'PY'

from pathlib import Path

p=Path(".ima/runtime/memory_bus.py")

if p.exists():
    print("MEMORY BUS OK")
else:
    print("MEMORY BUS MISSING")

PY



echo
echo "[6] Final service report"


cat > .ima/governance/service_layer_report.json <<EOF
{
 "system":"IMA",
 "status":"SERVICE_LAYER_CONNECTED",
 "service":"kernel/runtime/IMA_SERVICE_CORE_V1.js",
 "time":"$(date)"
}
EOF


echo
echo "=== IMA SERVICE LAYER COMPLETE ==="

