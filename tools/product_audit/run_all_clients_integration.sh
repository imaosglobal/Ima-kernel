#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA ALL CLIENTS INTEGRATION TEST ==="

PASS=0
FAIL=0

check_client() {
python - <<PY
from $1.app import status
r=status()

assert r["sdk"]["client"] is True
assert r["sdk"]["status"]=="READY"

print("[OK] $1")
PY
}

check_client product.apps.web
check_client product.apps.mobile
check_client product.apps.android
check_client product.apps.ios
check_client product.apps.linux

python - <<'PY'
from product.apps.shared.gateway_client import health

print("[SDK]", health())
print("[OK] Shared gateway verified")
PY

echo "=== ALL CLIENTS CONNECTED ==="
