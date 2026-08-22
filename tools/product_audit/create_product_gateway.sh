#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCT GATEWAY CREATION ==="

mkdir -p product/gateway
mkdir -p product/sdk
mkdir -p product/web
mkdir -p product/mobile
mkdir -p product/android

cat > product/gateway/product_gateway.py <<'PY'
import time

try:
    import ima_master_runtime
except Exception:
    ima_master_runtime = None


def ask(message):
    if ima_master_runtime:
        return ima_master_runtime.ask(message)

    return {
        "status": "fallback",
        "message": message
    }


def health():
    return {
        "product_gateway": True,
        "runtime_connected": ima_master_runtime is not None,
        "time": time.time()
    }
PY


cat > product/sdk/product_contract.json <<'JSON'
{
  "name": "IMA Product SDK",
  "version": "1.0",
  "transport": "HTTP",
  "core": "canonical-runtime",
  "clients": [
    "web",
    "mobile",
    "android"
  ],
  "endpoints": [
    "/health",
    "/ask"
  ]
}
JSON


cat > product/web/README.md <<'EOF'
IMA Web Client

React/Vite target.
Connects only through Product API.
EOF


cat > product/mobile/README.md <<'EOF'
IMA Mobile Client

Cross platform mobile interface.
Uses shared Product SDK.
EOF


cat > product/android/README.md <<'EOF'
IMA Android Native Layer

Device capabilities:
- sensors
- bluetooth
- local services

Connects through Product API.
EOF


cat > product/gateway/__init__.py <<'EOF'
EOF


echo "[CHECK] Import gateway"

python3 - <<'PY'
from product.gateway import product_gateway

PY


echo "=== PRODUCT GATEWAY READY ==="
