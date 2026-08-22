#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCT LAUNCHER ==="

mkdir -p product/launcher

cat > product/launcher/product_launcher.py <<'PY'
import json
import time
import subprocess
from pathlib import Path

def exists(path):
    return Path(path).exists()

def check_system():
    return {
        "gateway": exists(
            "product/gateway/product_gateway.py"
        ),
        "health": exists(
            "product/health/health_manager.py"
        ),
        "device": exists(
            "product/device/device_manager.py"
        ),
        "update": exists(
            "product/update/update_manager.py"
        ),
        "api": exists(
            "api/server.py"
        )
    }

def launch_status():
    checks = check_system()

    return {
        "product": "IMA",
        "status": "READY"
            if all(checks.values())
            else "INCOMPLETE",
        "components": checks,
        "time": time.time()
    }

if __name__ == "__main__":
        launch_status(),
        indent=2
    ))
PY


cat > product/launcher/launcher_registry.json <<'JSON'
{
  "name": "IMA Product Launcher",
  "version": "1.0",
  "entry": "product.launcher.product_launcher",
  "scope": "product-only",
  "core_access": "gateway-only"
}
JSON


cat > product/launcher/run_product.sh <<'RUN'
#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

echo "=== START IMA PRODUCT ==="

python3 -m product.launcher.product_launcher

echo "=== PRODUCT CHECK COMPLETE ==="
RUN


chmod +x product/launcher/run_product.sh


echo "[CHECK]"

./product/launcher/run_product.sh

echo "=== PRODUCT LAUNCHER READY ==="

