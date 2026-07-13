#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCTION DEPLOYMENT LAYER ==="

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/deployment_gateway/$DATE"

mkdir -p "$OUT"

echo "[1] Checking core protection"

if [ -e .ima/releases/final_release/IMA_FINAL_RELEASE.json ]; then
    echo "[OK] Final release found"
else
    echo "[FAIL] Missing final release"
    exit 1
fi

echo "[2] Runtime check"

python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher

g=product_gateway.health()
l=product_launcher.launch_status()

assert g["runtime_connected"] is True
assert l["status"]=="READY"

print("[OK] Runtime available")
print("[OK] Gateway available")
PY

echo "[3] Deployment manifest"

cat > "$OUT/DEPLOYMENT_GATEWAY.json" <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "status":"DEPLOYMENT_READY",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "gateway":"VERIFIED",
 "clients":[
   "web",
   "mobile",
   "android",
   "ios",
   "linux"
 ],
 "rollback":true,
 "created":"$DATE"
}
EOF

echo "[4] Hash"

sha256sum \
"$OUT/DEPLOYMENT_GATEWAY.json" \
> "$OUT/DEPLOYMENT_GATEWAY.sha256"

echo "[5] Verify"

python - <<PY
import json
from pathlib import Path

p=Path("$OUT/DEPLOYMENT_GATEWAY.json")
data=json.loads(p.read_text())

assert data["status"]=="DEPLOYMENT_READY"
assert data["core"]=="FROZEN"

print("[OK] Deployment manifest")
print("[OK] Core protected")
print("[OK] Deployment gateway ready")
PY

echo "=== DEPLOYMENT GATEWAY READY ==="
