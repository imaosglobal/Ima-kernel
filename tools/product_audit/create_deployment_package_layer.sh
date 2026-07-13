#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA DEPLOYMENT PACKAGE LAYER ==="

mkdir -p product/deployment
mkdir -p .ima/releases

cat > product/deployment/deployment_manager.py <<'PY'
import json
import time
from pathlib import Path

def exists(path):
    return Path(path).exists()

def collect_manifest():
    return {
        "product": "IMA",
        "version": "1.0",
        "runtime": exists("ima_master_runtime.py"),
        "gateway": exists(
            "product/gateway/product_gateway.py"
        ),
        "launcher": exists(
            "product/launcher/product_launcher.py"
        ),
        "health": exists(
            "product/health/health_manager.py"
        ),
        "clients": {
            "web": exists(
                "product/clients/web/client.json"
            ),
            "android": exists(
                "product/clients/android/client.json"
            ),
            "mobile": exists(
                "product/clients/mobile/client.json"
            )
        },
        "device": exists(
            "product/device/device_manager.py"
        ),
        "update": exists(
            "product/update/update_manager.py"
        ),
        "created": time.time()
    }

def save_release():
    manifest = collect_manifest()

    Path(
        ".ima/releases"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        ".ima/releases/IMA_RELEASE_MANIFEST.json"
    ).write_text(
        json.dumps(
            manifest,
            indent=2
        ),
        encoding="utf-8"
    )

    return manifest


if __name__ == "__main__":
    print(json.dumps(
        save_release(),
        indent=2
    ))
PY


cat > product/deployment/deployment_registry.json <<'JSON'
{
  "system": "IMA",
  "deployment_mode": "universal",
  "targets": [
    "web",
    "android",
    "mobile",
    "server"
  ],
  "core": "protected",
  "delivery": "gateway_based"
}
JSON


cat > product/deployment/build_release.sh <<'RUN'
#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

echo "=== BUILD IMA RELEASE ==="

python3 -m product.deployment.deployment_manager

echo "=== RELEASE MANIFEST CREATED ==="
RUN


chmod +x product/deployment/build_release.sh


echo "[CHECK]"

./product/deployment/build_release.sh

echo "=== DEPLOYMENT PACKAGE READY ==="

