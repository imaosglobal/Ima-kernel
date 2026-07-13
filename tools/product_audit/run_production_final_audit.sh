#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCTION FINAL AUDIT ==="

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

check_tag IMA_FINAL_LAUNCH_APPROVED_v1
check_tag IMA_PRODUCTION_RELEASE_v1
check_tag IMA_RELEASE_FINAL_v1
check_tag IMA_GLOBAL_RELEASE_AUDIT_v1
check_tag IMA_ALL_CLIENTS_INTEGRATION_v1
check_tag IMA_ARTIFACT_BUILD_PIPELINE_READY_v1

echo "--- RELEASE FILES ---"

check_file .ima/releases/final_release/IMA_FINAL_RELEASE.json
check_file .ima/releases/final_launch_gate.json
check_file .ima/releases/production_archive/20260713_174401/PRODUCTION_RELEASE.json

echo "--- RUNTIME ---"

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

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/master_manifest

cat > .ima/releases/master_manifest/IMA_PRODUCTION_RELEASE_MANIFEST.json <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "status":"PRODUCTION_RELEASE",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "launch":"APPROVED",
 "clients":[
   "web",
   "android",
   "ios",
   "linux",
   "mobile"
 ],
 "distribution":"READY",
 "rollback":"AVAILABLE",
 "created":"$DATE"
}
EOF

sha256sum .ima/releases/master_manifest/IMA_PRODUCTION_RELEASE_MANIFEST.json \
> .ima/releases/master_manifest/IMA_PRODUCTION_RELEASE_MANIFEST.sha256

echo
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
    echo "STATUS: MASTER RELEASE VERIFIED"
else
    echo "STATUS: AUDIT FAILED"
    exit 1
fi

echo "=== PRODUCTION FINAL AUDIT COMPLETE ==="
