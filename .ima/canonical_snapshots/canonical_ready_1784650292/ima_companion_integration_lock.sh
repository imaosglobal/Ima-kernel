#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA COMPANION INTEGRATION LOCK ==="

BRAIN="learning/meta_orchestrator.py"

mkdir -p product/mobile
mkdir -p .ima/governance

cat > product/mobile/mobile_layer.py <<PY
BRAIN="$BRAIN"

def connect():
    return {
        "layer":"mobile",
        "brain":BRAIN,
        "status":"connected"
    }

if __name__=="__main__":
    print(connect())
PY

cat > .ima/governance/COMPANION_LAYER_REGISTRY.json <<EOF
{
 "system":"IMA Companion Layer",
 "brain":"$BRAIN",
 "layers":{
   "voice":"product/voice",
   "mobile":"product/mobile",
   "childcare":"product/childcare",
   "safety":"product/safety",
   "device_bridge":"product/device_bridge",
   "identity":"product/identity",
   "memory":"memory"
 },
 "rule":"ALL_LAYERS_CONNECT_TO_SINGLE_BRAIN",
 "state":"LOCKED"
}
EOF


python3 - <<PY
from pathlib import Path
import json

reg=json.loads(
Path(".ima/governance/COMPANION_LAYER_REGISTRY.json").read_text()
)

assert Path(reg["brain"]).exists()

for k,v in reg["layers"].items():
    assert Path(v).exists(), f"missing {k}:{v}"

print("COMPANION REGISTRY OK")
print("LAYERS:",len(reg["layers"]))
PY


python3 -m py_compile product/mobile/mobile_layer.py

git add product/mobile \
.ima/governance/COMPANION_LAYER_REGISTRY.json

git commit -m "IMA companion layers integrated and locked"

git tag -a IMA_COMPANION_INTEGRATION_LOCK_v1 \
-m "All companion layers connected to canonical brain" || true

echo "=== COMPLETE ==="
