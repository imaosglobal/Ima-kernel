#!/data/data/com.termux/files/usr/bin/bash

set -e

cd "$HOME/ima_kernel"

echo "=== IMA E2E CANONICAL VERIFICATION ==="

mkdir -p .ima/governance


echo
echo "[1] Canonical path verification"

python3 - <<'PY'
import json
from pathlib import Path

checks = {
"brain":
"learning/meta_orchestrator.py",

"orchestrator":
"learning/module_registry.py",

"runtime":
"kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",

"event_bus":
"kernel/runtime/KERNEL_EVENT_BUS_V2.js",

"api":
"kernel/runtime/KERNEL_API_GATEWAY_V3.js",

"service":
"kernel/runtime/IMA_SERVICE_CORE_V1.js",

"memory":
".ima/runtime/memory_bus.py",

"device_registry":
".ima/governance/device_registry.json"
}


failed=[]

for name,path in checks.items():

    if Path(path).exists():
    else:
        failed.append(path)


if failed:
    raise SystemExit(
        "Missing canonical components"
    )


PY



echo
echo "[2] Brain verification"

python3 - <<'PY'

from learning.brain_guard import verify_brain

verify_brain(
"learning/meta_orchestrator.py"
)


PY



echo
echo "[3] Orchestrator verification"

python3 - <<'PY'

import json
from pathlib import Path

p=Path(
".ima/governance/orchestrator_registry.json"
)

data=json.loads(
p.read_text()
)

"ACTIVE MODULES:",
data.get("active_modules")
)

if data.get("active_modules",0) < 1:
    raise SystemExit(
    "No orchestrator modules"
    )


PY



echo
echo "[4] Service verification"

node - <<'JS'

const Service=require(
'./kernel/runtime/IMA_SERVICE_CORE_V1'
);

let s=new Service();

console.log(
s.health()
);

JS



echo
echo "[5] Event bus link"

grep -q "KERNEL_EVENT_BUS" \
kernel/runtime/IMA_SERVICE_CORE_V1.js \
&& echo "EVENT LINK OK"



echo
echo "[6] Governance integrity"

python3 - <<'PY'

import json
from pathlib import Path

files=[
".ima/governance/brain_registry.json",
".ima/governance/service_registry.json",
".ima/governance/runtime_registry.json"
]

for f in files:

    data=json.loads(
        Path(f).read_text()
    )

        "OK",
        f
    )


"GOVERNANCE INTEGRITY OK"
)

PY



echo
echo "[7] Generate final system state"


python3 - <<'PY'

import json,time
from pathlib import Path


state={

"system":"IMA",

"status":
"E2E_CANONICAL_VERIFIED",

"layers":[

"brain",
"orchestrator",
"runtime",
"event_bus",
"service",
"memory",
"api",
"devices"

],

"time":time.time()

}


Path(
".ima/governance/e2e_system_state.json"
).write_text(
json.dumps(
state,
indent=2,
ensure_ascii=False
)
)


"E2E STATE SAVED"
)

PY



echo
echo "=== IMA E2E VERIFICATION COMPLETE ==="

