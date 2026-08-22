#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA FULL PRODUCT VERIFICATION ==="

PASS=0
FAIL=0

check() {
    NAME="$1"
    PATH="$2"

    if [ -e "$PATH" ]; then
        echo "[OK] $NAME"
        PASS=$((PASS+1))
    else
        echo "[FAIL] $NAME"
        FAIL=$((FAIL+1))
    fi
}


echo "--- CORE ---"

check "conversation layer" "conversation_layer.py"
check "canonical start" "IMA_START.py"
check "master runtime" "ima_master_runtime.py"
check "python bridge" "kernel/runtime/CANONICAL/python_bridge.py"


echo "--- GATEWAY ---"

check "product gateway" "product/gateway/product_gateway.py"


echo "--- LAUNCHER ---"

check "product launcher" "product/launcher/product_launcher.py"


echo "--- HEALTH ---"

check "health manager" "product/health/health_manager.py"


echo "--- DEPLOYMENT ---"

check "release manifest" ".ima/releases/IMA_RELEASE_MANIFEST.json"
check "deployment manager" "product/deployment/deployment_manager.py"


echo "--- VERSION ---"

check "version manager" "product/version/version_manager.py"


echo "--- CLIENTS ---"

check "web client" "product/clients/web/client.json"
check "android client" "product/clients/android/client.json"
check "mobile client" "product/clients/mobile/client.json"


echo "--- DEVICE ---"

check "device manager" "product/device/device_manager.py"


echo "--- RUNTIME TEST ---"

/data/data/com.termux/files/usr/bin/python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher
from product.version.version_manager import current


PY


echo
echo "=== SUMMARY ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"


if [ "$FAIL" -eq 0 ]; then
    echo "STATUS: PRODUCT READY"
else
    echo "STATUS: PRODUCT INCOMPLETE"
    exit 1
fi

echo "=== VERIFICATION COMPLETE ==="

