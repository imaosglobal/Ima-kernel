#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA CORE <-> PRODUCT INTEGRATION TEST ==="

PASS=0
FAIL=0

ok() {
    echo "[OK] $1"
    PASS=$((PASS+1))
}

fail() {
    echo "[FAIL] $1"
    FAIL=$((FAIL+1))
}

echo "--- CORE IMPORT ---"

/data/data/com.termux/files/usr/bin/python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher
from product.version.version_manager import current

import conversation_layer
import ima_master_runtime


result = product_gateway.ask("IMA core product integration test")


if not result:
    raise SystemExit(1)

PY

echo
echo "--- PRODUCT FILES ---"

for f in \
product/gateway/product_gateway.py \
product/launcher/product_launcher.py \
product/health/health_manager.py \
product/device/device_manager.py \
product/update/update_manager.py \
product/version/version_manager.py
do
    if [ -e "$f" ]; then
        ok "$f"
    else
        fail "$f"
    fi
done


echo
echo "=== SUMMARY ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
    echo "STATUS: CORE AND PRODUCT CONNECTED"
else
    echo "STATUS: INTEGRATION FAILED"
    exit 1
fi

echo "=== INTEGRATION COMPLETE ==="

