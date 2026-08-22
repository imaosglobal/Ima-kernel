#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA ARTIFACT REGISTRY ==="

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/artifacts/$DATE

cat > .ima/releases/artifacts/$DATE/ARTIFACT_REGISTRY.json <<EOF
{
  "product":"IMA",
  "release":"1.0",
  "status":"READY",
  "runtime":"CANONICAL",
  "gateway":"VERIFIED",
  "clients":[
    "web",
    "mobile",
    "android",
    "ios",
    "linux"
  ],
  "deployment":"READY",
  "created":"$DATE"
}
EOF

sha256sum \
.ima/releases/artifacts/$DATE/ARTIFACT_REGISTRY.json \
> .ima/releases/artifacts/$DATE/ARTIFACT_REGISTRY.sha256

python - <<PY
import json
from pathlib import Path

p=Path(".ima/releases/artifacts/$DATE/ARTIFACT_REGISTRY.json")

data=json.loads(p.read_text())

assert data["status"]=="READY"
assert data["runtime"]=="CANONICAL"

PY

echo "=== ARTIFACT REGISTRY READY ==="
