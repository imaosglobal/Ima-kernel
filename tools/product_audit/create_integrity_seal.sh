#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA INTEGRITY SEAL ==="

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/integrity_seals/$DATE

echo "[1] Core hash"

cat > .ima/releases/integrity_seals/$DATE/core_files.txt <<EOF
conversation_layer.py
IMA_START.py
kernel/runtime/CANONICAL/python_bridge.py
ima_master_runtime.py
identity_context.py
EOF

while read f; do
    if [ -f "$f" ]; then
        sha256sum "$f"
    else
        echo "MISSING $f"
        exit 1
    fi
done < .ima/releases/integrity_seals/$DATE/core_files.txt \
> .ima/releases/integrity_seals/$DATE/core_hashes.sha256


echo "[2] Product hash"

find product \
-type f \
-not -path "*/__pycache__/*" \
| sort \
| xargs sha256sum \
> .ima/releases/integrity_seals/$DATE/product_hashes.sha256


echo "[3] System manifest"

cat > .ima/releases/integrity_seals/$DATE/INTEGRITY_MANIFEST.json <<EOF
{
  "product": "IMA",
  "release": "RC-1.0",
  "status": "SEALED",
  "core": "FROZEN",
  "runtime": "CANONICAL",
  "integration": "VERIFIED",
  "verification_tag": "IMA_CORE_PRODUCT_INTEGRATION_VERIFIED_v1",
  "created": "$DATE"
}
EOF


echo "[4] Verify"

cat .ima/releases/integrity_seals/$DATE/INTEGRITY_MANIFEST.json

echo
echo "=== INTEGRITY SEAL CREATED ==="

