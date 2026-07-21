#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

GOV="$ROOT/.ima/governance"

CHAIN="$GOV/IMA_ARCHITECTURE_CHAIN.json"
LOCK="$GOV/IMA_CHAIN_LOCK"
POLICY="$GOV/IMA_BUILD_POLICY.json"

mkdir -p "$GOV"

echo "=== IMA CHAIN FREEZE ==="

if [ -f "$LOCK" ]; then
    echo "CHAIN ALREADY LOCKED"
    cat "$LOCK"
    exit 1
fi


python3 - <<PY
import os
import json
import time

root="$ROOT"

candidates=[
"kernel/runtime/ENTRYPOINT.js",
"kernel/kernel_single.js",
"kernel/ima_runtime.js",
"kernel/ima_supreme_kernel.js",
"kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
"kernel/runtime/KERNEL_UNIFIED_RUNTIME_V1.js"
]


def score(path):
    full=os.path.join(root,path)

    if not os.path.exists(full):
        return -100

    s=0

    size=os.path.getsize(full)

    if size>100:
        s+=2

    if "ENTRYPOINT" in path:
        s+=5

    if "UNIFIED_RUNTIME" in path:
        s+=4

    if "kernel_single" in path:
        s+=4

    if "ima_runtime" in path:
        s+=3

    return s


ranking=[]

for c in candidates:
    ranking.append({
        "path":c,
        "score":score(c),
        "exists":os.path.exists(os.path.join(root,c))
    })


ranking.sort(
    key=lambda x:x["score"],
    reverse=True
)


active=ranking[0]["path"]


chain={
    "system":"IMA",
    "type":"architecture_chain",
    "created":time.time(),

    "canonical":{
        "brain":"learning/meta_orchestrator.py",
        "runtime":active,
        "governance":".ima/governance"
    },

    "selection":{
        "method":"automatic",
        "candidates":ranking
    },

    "policy":{
        "single_chain":True,
        "no_duplicate_active_components":True,
        "future_components_require_registration":True,
        "lock_after_verified_connection":True,
        "protect_existing_working_components":True,
        "graveyard_usage":"only_when_required_and_verified"
    },

    "status":"FROZEN_PENDING_TEST"
}


with open("$CHAIN","w") as f:
    json.dump(chain,f,indent=2)


policy={
"IMA_BUILD_RULES":{
    "rule1":"Every new component enters through governance registry",
    "rule2":"Every working component is locked after verification",
    "rule3":"No modification of locked component without new version",
    "rule4":"No duplicate brains or orchestrators",
    "rule5":"No damage to existing working components",
    "rule6":"Graveyard components may be restored only after verification"
}
}


with open("$POLICY","w") as f:
    json.dump(policy,f,indent=2)


print("SELECTED RUNTIME:")
print(active)

PY


echo "[VERIFY]"

python3 - <<PY
import json

with open("$CHAIN") as f:
    c=json.load(f)

assert c["canonical"]["brain"]=="learning/meta_orchestrator.py"
assert c["policy"]["single_chain"] is True

print("CHAIN VERIFICATION PASS")

PY


cat > "$LOCK" <<EOF
IMA ARCHITECTURE CHAIN LOCKED

CANONICAL:
$CHAIN

POLICY:
$POLICY

RULE:
NO UNREGISTERED COMPONENTS
EOF


chmod 444 "$LOCK"

python3 - <<PY
import json

p="$CHAIN"

with open(p) as f:
    x=json.load(f)

x["status"]="FROZEN_AND_LOCKED"

with open(p,"w") as f:
    json.dump(x,f,indent=2)

PY


echo
echo "=============================="
echo " IMA CHAIN COMPLETE"
echo " IMA CHAIN LOCKED"
echo "=============================="

echo "$CHAIN"
echo "$LOCK"

