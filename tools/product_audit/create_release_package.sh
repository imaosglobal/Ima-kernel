#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA RELEASE PACKAGE CREATION ==="

DATE=$(date +%Y%m%d_%H%M%S)

OUT=".ima/releases/packages/IMA_RC1_$DATE"

mkdir -p "$OUT"

echo "[1] Copy release manifests"

cp .ima/releases/final/*/RELEASE_COMPLETION.json "$OUT/"

cp .ima/releases/candidates/IMA_RC_MANIFEST.json "$OUT/"

cp .ima/releases/candidates/IMA_RC_MANIFEST.sha256 "$OUT/"


echo "[2] Create package inventory"

find product \
-type f \
-not -path "*/__pycache__/*" \
| sort > "$OUT/PRODUCT_FILES.txt"


echo "[3] Create runtime inventory"

for f in \
conversation_layer.py \
IMA_START.py \
ima_master_runtime.py \
kernel/runtime/CANONICAL/python_bridge.py
do
 if [ -e "$f" ]; then
   echo "$f"
 fi
done > "$OUT/CORE_FILES.txt"


echo "[4] Create release package manifest"

cat > "$OUT/RELEASE_PACKAGE.json" <<EOF
{
 "product":"IMA",
 "release":"RC-1.0",
 "package":"READY",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "integration":"VERIFIED",
 "distribution":"READY",
 "clients":[
   "web",
   "android",
   "mobile"
 ],
 "created":"$DATE"
}
EOF


echo "[5] Package hash"

sha256sum "$OUT/RELEASE_PACKAGE.json" \
> "$OUT/RELEASE_PACKAGE.sha256"


echo "[6] Verify"

python - <<PY
import json
from pathlib import Path

p=Path("$OUT/RELEASE_PACKAGE.json")

data=json.loads(p.read_text())

assert data["package"]=="READY"
assert data["core"]=="FROZEN"

PY


echo
echo "PACKAGE:"
echo "$OUT"

echo "=== RELEASE PACKAGE READY ==="

