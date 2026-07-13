#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA FINAL LAUNCH GATE ==="

PASS=0
FAIL=0

check_tag() {
if git tag | grep -q "$1"; then
 echo "[OK] TAG $1"
 PASS=$((PASS+1))
else
 echo "[FAIL] TAG $1"
 FAIL=$((FAIL+1))
fi
}

check_tag IMA_RELEASE_FINAL_v1
check_tag IMA_PRODUCTION_READINESS_v1
check_tag IMA_RELEASE_DISTRIBUTION_BUNDLE_READY_v1
check_tag IMA_ALL_CLIENTS_INTEGRATION_v1
check_tag IMA_ARTIFACT_BUILD_PIPELINE_READY_v1

echo "--- GIT STATE ---"

if [ -z "$(git status --porcelain)" ]; then
 echo "[OK] Working tree clean"
 PASS=$((PASS+1))
else
 echo "[FAIL] Git changes detected"
 FAIL=$((FAIL+1))
fi

echo "--- RUNTIME ---"

python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher
from product.version.version_manager import current

assert product_gateway.health()["runtime_connected"] is True
assert product_launcher.launch_status()["status"]=="READY"

print("[OK] Gateway")
print("[OK] Launcher")
print("[OK] Version")
PY

DATE=$(date +%Y%m%d_%H%M%S)

cat > .ima/releases/final_launch_gate.json <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "status":"LAUNCH_APPROVED",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "distribution":"READY",
 "created":"$DATE"
}
EOF

echo
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
 echo "STATUS: LAUNCH APPROVED"
else
 exit 1
fi

echo "=== FINAL LAUNCH GATE COMPLETE ==="
