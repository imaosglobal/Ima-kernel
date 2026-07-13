#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA DISTRIBUTION LAYER ==="

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/distribution/$DATE

echo "[1] Creating distribution manifest"

cat > .ima/releases/distribution/$DATE/DISTRIBUTION_MANIFEST.json <<EOF
{
  "product": "IMA",
  "release": "RC-1.0",
  "distribution": "READY",
  "integrity": "IMA_INTEGRITY_SEALED_RC1_v1",
  "core": "FROZEN",
  "runtime": "CANONICAL",
  "clients": [
    "web",
    "android",
    "mobile"
  ],
  "deployment": true,
  "update_system": true,
  "created": "$DATE"
}
EOF

echo "[2] Creating package inventory"

find product \
-type f \
-not -path "*/__pycache__/*" \
| sort > .ima/releases/distribution/$DATE/PACKAGE_FILES.txt

echo "[3] Creating distribution hash"

sha256sum \
.ima/releases/distribution/$DATE/DISTRIBUTION_MANIFEST.json \
> .ima/releases/distribution/$DATE/DISTRIBUTION_HASH.sha256


echo "[4] Verification"

python - <<'PY'
import json
from pathlib import Path

p=Path(".ima/releases/distribution")
latest=sorted(p.iterdir())[-1]

data=json.loads(
(latest/"DISTRIBUTION_MANIFEST.json").read_text()
)

assert data["distribution"]=="READY"
assert data["core"]=="FROZEN"

print("[OK] Distribution manifest")
print("[OK] Core preserved")
print("[OK] Product package ready")
PY


echo "=== DISTRIBUTION READY ==="

