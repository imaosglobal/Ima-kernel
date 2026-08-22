#!/data/data/com.termux/files/usr/bin/bash

set -e

cd "$HOME/ima_kernel"

echo "=== IMA PRODUCT LAYER CANONICAL LOCK ==="

mkdir -p .ima/governance


python3 - <<'PY'
import json
import time
from pathlib import Path


root=Path(".")


def first_existing(paths):
    for p in paths:
        if Path(p).exists():
            return p
    return None


layers={

"identity":
[
"kernel/services/identity.js",
"kernel/api/auth.js",
"kernel/_graveyard/_archive/releases__v1778001671191__auth_layer.js"
],

"api":
[
"kernel/runtime/KERNEL_API_GATEWAY_V3.js",
"kernel/runtime/KERNEL_API_GATEWAY_V2.js",
"server.js"
],

"ui":
[
"android",
"frontend",
"src",
"app"
],

"voice":
[
"kernel/services/voice.js",
"learning/voice_engine.py",
".ima/voice.json"
],

"child_safety":
[
"learning/child_safety_engine.py",
"learning/safety_gate.py"
],

"device":
[
".ima/governance/device_registry.json",
"kernel/ima_devices/index.js"
],

"deployment":
[
"docker-compose.yml",
"Dockerfile",
"deploy.js"
]

}


canonical={}

for name,paths in layers.items():

    selected=first_existing(paths)

    canonical[name]={
        "status":
        "CONNECTED" if selected else "MISSING",

        "canonical_path":
        selected,

        "alternatives_checked":
        paths
    }


registry={

"system":"IMA",

"state":
"PRODUCT_LAYER_LOCKED",

"brain":
"learning/meta_orchestrator.py",

"orchestrator":
"learning/module_registry.py",

"service_core":
"kernel/runtime/IMA_SERVICE_CORE_V1.js",

"layers":
canonical,

"policy":[

"single_product_layer_only",
"reuse_existing_components",
"block_duplicate_services",
"redirect_to_canonical_path"

],

"time":
time.time()

}


Path(
".ima/governance/product_layer_registry.json"
).write_text(
json.dumps(
registry,
indent=2,
ensure_ascii=False
),
encoding="utf-8"
)


Path(
".ima/governance/product_layer_lock.json"
).write_text(
json.dumps(
{
"locked":True,
"rule":
"NO_DUPLICATE_PRODUCT_COMPONENTS",
"time":time.time()
},
indent=2
),
encoding="utf-8"
)


for k,v in canonical.items():
        k,
        "=>",
        v["status"],
        v["canonical_path"]
    )


"PRODUCT LAYER GOVERNANCE SAVED"
)

PY


echo
echo "[2] Verify core chain"


python3 - <<'PY'

from learning.brain_guard import verify_brain

verify_brain(
"learning/meta_orchestrator.py"
)

"BRAIN OK"
)

PY


echo
echo "[3] Product registry"

cat .ima/governance/product_layer_registry.json


echo
echo "=== IMA PRODUCT LAYER LOCK COMPLETE ==="

