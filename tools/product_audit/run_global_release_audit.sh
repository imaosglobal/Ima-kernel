#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA GLOBAL RELEASE AUDIT ==="

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

check_file() {
    if [ -e "$1" ]; then
        echo "[OK] FILE $1"
        PASS=$((PASS+1))
    else
        echo "[FAIL] FILE $1"
        FAIL=$((FAIL+1))
    fi
}

echo "--- RELEASE TAGS ---"

check_tag IMA_CORE_PRODUCT_INTEGRATION_VERIFIED_v1
check_tag IMA_INTEGRITY_SEALED_RC1_v1
check_tag IMA_DISTRIBUTION_READY_v1
check_tag IMA_CLIENT_BUILD_VERIFIED_v1
check_tag IMA_RELEASE_PACKAGE_v1
check_tag IMA_PRODUCTION_READINESS_v1
check_tag IMA_RELEASE_FINAL_v1
check_tag IMA_ALL_CLIENTS_INTEGRATION_v1
check_tag IMA_CLIENT_DEPLOYMENT_READY_v1
check_tag IMA_ARTIFACT_REGISTRY_CLEAN_v1


echo "--- MANIFESTS ---"

check_file .ima/releases/final_release/IMA_FINAL_RELEASE.json
check_file .ima/releases/PRODUCTION_READINESS.json
check_file .ima/releases/final_release/IMA_FINAL_RELEASE.sha256


echo "--- RUNTIME ---"

python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher
from product.version.version_manager import current


assert product_gateway.health()["runtime_connected"] is True
assert product_launcher.launch_status()["status"]=="READY"

PY


echo
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
    echo "STATUS: GLOBAL RELEASE READY"
else
    echo "STATUS: AUDIT FAILED"
    exit 1
fi

echo "=== GLOBAL AUDIT COMPLETE ==="
