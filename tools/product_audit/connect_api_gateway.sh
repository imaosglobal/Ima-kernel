#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== CONNECT API TO PRODUCT GATEWAY ==="

cp api/server.py .ima/runtime_snapshots/api_before_gateway_$(date +%Y%m%d_%H%M%S).py

python3 - <<'PY'
from pathlib import Path

p=Path("api/server.py")
s=p.read_text()

if "product_gateway" not in s:
    s=s.replace(
        "import",
        "from product.gateway import product_gateway\n\nimport",
        1
    )

    s=s.replace(
        "ima_master_runtime.ask(question)",
        "product_gateway.ask(question)"
    )

    p.write_text(s)

PY

python3 - <<'PY'
import api.server
PY

echo "=== API GATEWAY CONNECTED ==="
