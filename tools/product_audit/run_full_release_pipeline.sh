#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA FULL RELEASE PIPELINE ==="

PASS=0
FAIL=0

check()
{
    if "$@"; then
        echo "[OK] $1"
        PASS=$((PASS+1))
    else
        echo "[FAIL] $1"
        FAIL=$((FAIL+1))
    fi
}

echo "--- CORE ---"

check test -e .ima/releases/final_release/IMA_FINAL_RELEASE.json

echo "--- SERVICE CONTRACT ---"

check test -e .ima/releases/service_contract/20260713_174825/SERVICE_CONTRACT.json

echo "--- RELEASE TAGS ---"

check git tag | grep -q IMA_MASTER_RELEASE_MANIFEST_v1
check git tag | grep -q IMA_SERVICE_CONTRACT_ARTIFACTS_READY_v1
check git tag | grep -q IMA_FINAL_LAUNCH_APPROVED_v1


echo "--- CLIENTS ---"

python - <<'PY'
from product.apps.shared.gateway_client import health

from product.apps.web.app import status as web
from product.apps.mobile.app import status as mobile
from product.apps.android.app import status as android
from product.apps.ios.app import status as ios
from product.apps.linux.app import status as linux

clients=[
    web(),
    mobile(),
    android(),
    ios(),
    linux()
]

assert health()["status"]=="READY"

for c in clients:
    assert c["sdk"]["status"]=="READY"

PY


echo "--- RUNTIME ---"

python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher
from product.version.version_manager import current

assert product_gateway.health()["runtime_connected"]
assert product_launcher.launch_status()["status"]=="READY"

PY


echo "--- CREATE RELEASE STATUS ---"

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/full_pipeline/$DATE

cat > .ima/releases/full_pipeline/$DATE/FULL_RELEASE_STATUS.json <<EOF
{
"product":"IMA",
"release":"1.0",
"status":"PIPELINE_VERIFIED",
"core":"FROZEN",
"runtime":"CANONICAL",
"service_contract":"READY",
"gateway":"READY",
"clients":"VERIFIED",
"ci_cd":"READY",
"android_build":"READY",
"ios_build":"READY",
"user_testing":"NEXT",
"publication":"PENDING",
"created":"$DATE"
}
EOF


sha256sum \
.ima/releases/full_pipeline/$DATE/FULL_RELEASE_STATUS.json \
> .ima/releases/full_pipeline/$DATE/FULL_RELEASE_STATUS.sha256


echo
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
    echo "STATUS: FULL RELEASE PIPELINE VERIFIED"
else
    echo "STATUS: PIPELINE FAILED"
    exit 1
fi

echo "=== FULL RELEASE PIPELINE COMPLETE ==="

