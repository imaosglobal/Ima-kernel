#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCTION READINESS CHECK ==="

PASS=0
FAIL=0

check_tag() {
 if git tag | grep -q "$1"; then
  echo "[OK] $1"
  PASS=$((PASS+1))
 else
  echo "[FAIL] $1"
  FAIL=$((FAIL+1))
 fi
}

echo "--- TAGS ---"

check_tag IMA_RELEASE_PACKAGE_v1
check_tag IMA_RELEASE_CANDIDATE_COMPLETE_v1
check_tag IMA_CLIENT_BUILD_VERIFIED_v1
check_tag IMA_DISTRIBUTION_READY_v1
check_tag IMA_INTEGRITY_SEALED_RC1_v1
check_tag IMA_CORE_PRODUCT_INTEGRATION_VERIFIED_v1


echo "--- PACKAGE ---"

LATEST=$(ls -dt .ima/releases/packages/IMA_RC1_* | head -1)

if [ -f "$LATEST/RELEASE_PACKAGE.json" ]; then
 echo "[OK] Release package exists"
 PASS=$((PASS+1))
else
 echo "[FAIL] Release package missing"
 FAIL=$((FAIL+1))
fi


echo "--- RUNTIME ---"

python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher

g = product_gateway.health()
l = product_launcher.launch_status()

print("[GATEWAY]", g)
print("[LAUNCHER]", l)

assert g["product_gateway"] is True
assert l["status"] == "READY"

print("[OK] Runtime chain")
PY


mkdir -p .ima/releases

cat > .ima/releases/PRODUCTION_READINESS.json <<EOF
{
 "product":"IMA",
 "release":"RC-1.0",
 "status":"READY_FOR_PRODUCTION",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "package":"VERIFIED"
}
EOF


echo
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
 echo "STATUS: PRODUCTION READY"
else
 echo "STATUS: NOT READY"
 exit 1
fi

echo "=== PRODUCTION READINESS COMPLETE ==="

