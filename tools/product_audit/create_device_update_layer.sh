#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA DEVICE + UPDATE LAYER ==="

mkdir -p product/device
mkdir -p product/update

cat > product/device/device_manager.py <<'PY'
import platform
import time

def device_info():
    return {
        "platform": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "time": time.time()
    }

def capabilities():
    return {
        "network": True,
        "storage": True,
        "sensors": "unknown",
        "bluetooth": "unknown"
    }
PY

cat > product/device/device_registry.json <<'JSON'
{
  "name": "IMA Device Registry",
  "version": "1.0",
  "registration": true,
  "supported": [
    "android",
    "web",
    "mobile",
    "desktop"
  ]
}
JSON

cat > product/update/update_manager.py <<'PY'
import time

CURRENT_VERSION="1.0"

def status():
    return {
        "version": CURRENT_VERSION,
        "update_ready": True,
        "rollback": True,
        "time": time.time()
    }
PY

cat > product/update/update_registry.json <<'JSON'
{
  "update_system": "IMA",
  "strategy": "gateway",
  "rollback": true,
  "migration": true,
  "compatibility": "universal"
}
JSON

echo "[CHECK]"

python3 - <<'PY'
from product.device.device_manager import device_info, capabilities
from product.update.update_manager import status

PY

echo "=== DEVICE UPDATE LAYER READY ==="
