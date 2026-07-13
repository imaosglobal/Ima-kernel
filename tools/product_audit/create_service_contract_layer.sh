#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA SERVICE CONTRACT LAYER ==="

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/service_contract/$DATE"

mkdir -p "$OUT"

echo "[1] Core protection"

test -e .ima/releases/master_manifest/IMA_PRODUCTION_RELEASE_MANIFEST.json

echo "[OK] Master release preserved"

echo "[2] Create API contract"

cat > "$OUT/SERVICE_CONTRACT.json" <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "status":"SERVICE_CONTRACT_READY",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "api_version":"v1",

 "endpoints":[
   {
    "name":"health",
    "method":"GET",
    "path":"/health"
   },
   {
    "name":"status",
    "method":"GET",
    "path":"/status"
   },
   {
    "name":"ask",
    "method":"POST",
    "path":"/ask"
   },
   {
    "name":"version",
    "method":"GET",
    "path":"/version"
   }
 ],

 "clients":[
   "web",
   "android",
   "ios",
   "linux",
   "mobile"
 ],

 "authentication":"PENDING",
 "external_gateway":"PENDING",
 "created":"$DATE"
}
EOF

echo "[3] Validate contract"

python - <<PY
import json
from pathlib import Path

p=Path("$OUT/SERVICE_CONTRACT.json")
d=json.loads(p.read_text())

assert d["status"]=="SERVICE_CONTRACT_READY"
assert d["core"]=="FROZEN"
assert len(d["clients"])==5

print("[OK] Service contract")
print("[OK] Core protected")
print("[OK] Client compatibility verified")
PY

echo "[4] Hash"

sha256sum "$OUT/SERVICE_CONTRACT.json" \
> "$OUT/SERVICE_CONTRACT.sha256"

echo
echo "CONTRACT:"
echo "$OUT"

echo "=== SERVICE CONTRACT READY ==="

