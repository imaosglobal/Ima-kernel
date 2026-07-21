#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
GOV="$ROOT/.ima/governance"
LOCK="$GOV/IMA_GLOBAL_PRODUCT_AUDIT.lock"
MAP="$GOV/IMA_GLOBAL_PRODUCT_MAP.json"

mkdir -p "$GOV"

echo "=== IMA GLOBAL PRODUCT AUDIT ==="

if [ -f "$LOCK" ]; then
    echo "AUDIT LOCK EXISTS"
    echo "Canonical audit already created:"
    cat "$LOCK"
    exit 1
fi

echo "[1] Scanning project..."

python3 - <<PY
import os, json, time

root="$ROOT"

categories={
    "brain":[],
    "runtime":[],
    "kernel":[],
    "memory":[],
    "device":[],
    "safety":[],
    "product":[]
}

for base,dirs,files in os.walk(root):
    for f in files:
        p=os.path.join(base,f)

        low=p.lower()

        if "orchestrator" in low or "brain" in low:
            categories["brain"].append(p)

        if "runtime" in low:
            categories["runtime"].append(p)

        if "kernel" in low:
            categories["kernel"].append(p)

        if "memory" in low:
            categories["memory"].append(p)

        if "device" in low:
            categories["device"].append(p)

        if "safety" in low or "guard" in low:
            categories["safety"].append(p)

        if "product" in low or "app" in low:
            categories["product"].append(p)

result={
    "system":"IMA",
    "type":"global_product_audit",
    "created":time.time(),
    "canonical":True,
    "locked":True,
    "categories":categories,
    "policy":{
        "single_audit":True,
        "block_duplicate_creation":True
    }
}

with open("$MAP","w") as f:
    json.dump(result,f,indent=2)

with open("$LOCK","w") as f:
    f.write(
        "IMA GLOBAL PRODUCT AUDIT LOCKED\n"
        "DO NOT CREATE ANOTHER AUDIT\n"
        "CANONICAL FILE:\n"
        ".ima/governance/IMA_GLOBAL_PRODUCT_MAP.json\n"
    )

print("AUDIT CREATED")
print("$MAP")
PY

chmod 444 "$LOCK"
chmod 755 "$0"

echo
echo "=============================="
echo " IMA AUDIT LOCKED"
echo "=============================="
echo "Canonical:"
echo "$MAP"
echo "Lock:"
echo "$LOCK"
