#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA UNIVERSAL CLIENT LAYER ==="

mkdir -p product/clients/web
mkdir -p product/clients/android
mkdir -p product/clients/mobile
mkdir -p product/device
mkdir -p product/update

cat > product/clients/client_contract.json <<'JSON'
{
  "name": "IMA Universal Client Contract",
  "version": "1.0",
  "transport": "HTTP",
  "gateway": "product.gateway.product_gateway",
  "targets": [
    "web",
    "android",
    "mobile"
  ]
}
JSON

cat > product/clients/web/client.json <<'JSON'
{
  "platform": "web",
  "connection": "product_gateway",
  "status": "ready"
}
JSON

cat > product/clients/android/client.json <<'JSON'
{
  "platform": "android",
  "connection": "product_gateway",
  "status": "ready"
}
JSON

cat > product/clients/mobile/client.json <<'JSON'
{
  "platform": "mobile",
  "connection": "product_gateway",
  "status": "ready"
}
JSON

cat > product/device/capability_registry.json <<'JSON'
{
  "device_layer": "IMA",
  "capabilities": [
    "camera",
    "microphone",
    "bluetooth",
    "sensors",
    "storage",
    "network"
  ]
}
JSON

cat > product/update/update_protocol.json <<'JSON'
{
  "versioning": true,
  "migration": true,
  "rollback": true,
  "compatibility": "gateway_based"
}
JSON

echo "[CHECK]"

python3 - <<'PY'
import json
from pathlib import Path

files=[
"product/clients/client_contract.json",
"product/clients/web/client.json",
"product/clients/android/client.json",
"product/clients/mobile/client.json",
"product/device/capability_registry.json",
"product/update/update_protocol.json"
]

for f in files:
    json.loads(Path(f).read_text())
PY

echo "=== UNIVERSAL CLIENT LAYER READY ==="
