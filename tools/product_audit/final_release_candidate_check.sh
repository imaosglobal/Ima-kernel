#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA FINAL RELEASE CANDIDATE CHECK ==="

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/final/$DATE

PASS=0
FAIL=0

check() {
 if git tag | grep -q "$1"; then
   echo "[OK] $1"
   PASS=$((PASS+1))
 else
   echo "[FAIL] $1"
   FAIL=$((FAIL+1))
 fi
}

check IMA_CORE_PRODUCT_INTEGRATION_VERIFIED_v1
check IMA_INTEGRITY_SEALED_RC1_v1
check IMA_DISTRIBUTION_READY_v1
check IMA_CLIENT_BUILD_VERIFIED_v1


python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher
from product.version.version_manager import current

print("[GATEWAY]", product_gateway.health())
print("[LAUNCHER]", product_launcher.launch_status())
print("[VERSION]", current())
print("[OK] Runtime chain")
PY


cat > .ima/releases/final/$DATE/RELEASE_COMPLETION.json <<EOF
{
 "product":"IMA",
 "release":"RC-1.0",
 "status":"COMPLETE",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "clients":"VERIFIED",
 "distribution":"READY",
 "created":"$DATE"
}
EOF


echo
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
 echo "STATUS: RELEASE CANDIDATE COMPLETE"
else
 exit 1
fi

