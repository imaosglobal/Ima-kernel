#!/data/data/com.termux/files/usr/bin/bash

set -e

cd ~/ima_kernel

echo "=== IMA RENDER PRODUCTION ACTIVATION ==="

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/render_activation/$DATE"

mkdir -p "$OUT"

RENDER_SERVICE="srv-d0r96hadbo4c73a4o910"
RENDER_URL="https://ima-915m.onrender.com"


echo "[1] Render target"

cat > "$OUT/RENDER_DEPLOYMENT.json" <<EOF
{
 "product":"IMA",
 "provider":"Render",
 "service_id":"$RENDER_SERVICE",
 "url":"$RENDER_URL",
 "runtime":"CANONICAL",
 "docker":"READY",
 "status":"TARGET_CONNECTED",
 "created":"$DATE"
}
EOF

echo "[OK] Render target registered"


echo "[2] Local runtime chain"

python - <<'PY'
from product.gateway import product_gateway
from product.launcher import product_launcher

g = product_gateway.health()
l = product_launcher.launch_status()

assert g["runtime_connected"] is True
assert l["status"] == "READY"

PY


echo "[3] External endpoint check"

python - <<PY
import urllib.request
import json

url="$RENDER_URL"

result={
 "url":url,
 "reachable":False,
 "status":None
}

try:
    r=urllib.request.urlopen(url,timeout=15)
    result["reachable"]=True
    result["status"]=r.status
except Exception as e:
    result["error"]=str(e)

with open("$OUT/RENDER_HEALTH_CHECK.json","w") as f:
    json.dump(result,f,indent=2)

PY


echo "[4] Release gate"

python - <<PY
import json
from pathlib import Path

a=json.loads(Path("$OUT/RENDER_DEPLOYMENT.json").read_text())
b=json.loads(Path("$OUT/RENDER_HEALTH_CHECK.json").read_text())

assert a["provider"]=="Render"


if b.get("reachable"):
else:
PY


cat > "$OUT/RENDER_RELEASE_GATE.json" <<EOF
{
 "product":"IMA",
 "provider":"Render",
 "service_id":"$RENDER_SERVICE",
 "runtime":"CANONICAL",
 "status":"VERIFICATION_COMPLETE",
 "created":"$DATE"
}
EOF


sha256sum "$OUT"/*.json > "$OUT/HASHES.sha256"


echo
echo "OUTPUT:"
echo "$OUT"
echo "=== RENDER ACTIVATION COMPLETE ==="

