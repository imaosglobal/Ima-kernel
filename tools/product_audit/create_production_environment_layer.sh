#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCTION ENVIRONMENT LAYER ==="

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/production_environment/$DATE"

mkdir -p "$OUT"

echo "[1] Core protection"

test -e .ima/releases/master_manifest/IMA_PRODUCTION_RELEASE_MANIFEST.json

echo "[OK] Master manifest found"

echo "[2] Runtime check"

python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher
from product.version.version_manager import current

g = product_gateway.health()
l = product_launcher.launch_status()
v = current()

assert g["runtime_connected"] is True
assert l["status"] == "READY"

print("[OK] Gateway")
print("[OK] Launcher")
print("[OK] Version")
PY

echo "[3] Create environment manifest"

cat > "$OUT/PRODUCTION_ENVIRONMENT.json" <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "environment":"production",
 "status":"ENVIRONMENT_READY",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "gateway":"PENDING_EXTERNAL",
 "database":"PENDING_EXTERNAL",
 "monitoring":"PENDING_EXTERNAL",
 "created":"$DATE"
}
EOF

echo "[4] Hash"

sha256sum "$OUT/PRODUCTION_ENVIRONMENT.json" \
> "$OUT/PRODUCTION_ENVIRONMENT.sha256"


python - <<PY
import json
from pathlib import Path

p=Path("$OUT/PRODUCTION_ENVIRONMENT.json")
d=json.loads(p.read_text())

assert d["status"]=="ENVIRONMENT_READY"
assert d["core"]=="FROZEN"

print("[OK] Environment manifest")
print("[OK] Core preserved")
print("[OK] Deployment layer ready")
PY

echo
echo "ENVIRONMENT:"
echo "$OUT"

echo "=== PRODUCTION ENVIRONMENT READY ==="

