#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"

cd "$ROOT"

echo "=== IMA PRODUCT ARCHITECTURE FINALIZATION ==="

mkdir -p \
 governance \
 .ima/governance \
 device \
 child_safety \
 product \
 boot \
 kernel/runtime

cat > .ima/governance/IMA_PRODUCT_ARCHITECTURE_LOCK.json <<'JSON'
{
  "system": "IMA",
  "architecture": "IMA_KERNEL_PRODUCT_ARCHITECTURE_v1",
  "state": "LOCKED",
  "brain": {
    "language": "Python",
    "canonical": "learning/meta_orchestrator.py"
  },
  "body": {
    "language": "JavaScript",
    "canonical": "kernel/runtime/ENTRYPOINT.js"
  },
  "rules": [
    "single_brain_only",
    "single_body_runtime_only",
    "no_duplicate_orchestrators",
    "no_duplicate_entrypoints",
    "redirect_to_canonical_path"
  ],
  "purpose": "global human assistant architecture",
  "locked": true
}
JSON


cat > device/device_manager.py <<'PY'
class DeviceManager:
    def __init__(self):
        self.devices = []

    def register(self, device):
        self.devices.append(device)

    def list_devices(self):
        return self.devices
PY


cat > child_safety/child_safety_core.py <<'PY'
class ChildSafetyCore:
    def evaluate(self, context):
        return {
            "safe": True,
            "mode": "child_protection"
        }
PY


cat > product/product_runtime.py <<'PY'
class ProductRuntime:
    def status(self):
        return {
            "product": "IMA",
            "architecture": "v1"
        }
PY


cat > boot/IMA_ENTRYPOINT.py <<'PY'
from learning.meta_orchestrator import *

def boot():
    return {
        "system": "IMA",
        "brain": "Python",
        "status": "online"
    }

if __name__ == "__main__":
PY


cat > .ima/governance/CANONICAL_ARCHITECTURE.json <<'JSON'
{
  "canonical": true,
  "brain": "learning/meta_orchestrator.py",
  "body": "kernel/runtime/ENTRYPOINT.js",
  "product_architecture": "IMA_KERNEL_PRODUCT_ARCHITECTURE_v1"
}
JSON


python3 - <<'PY'
import json
from pathlib import Path

files=[
".ima/governance/IMA_PRODUCT_ARCHITECTURE_LOCK.json",
".ima/governance/CANONICAL_ARCHITECTURE.json"
]

for f in files:
    json.load(open(f))

PY


git add .

git commit -m "IMA product architecture v1 Python brain JS body locked"

git tag -a IMA_KERNEL_PRODUCT_ARCHITECTURE_v1 \
-m "Python brain JS body architecture locked"

echo "=== IMA PRODUCT ARCHITECTURE LOCKED ==="
echo "BRAIN: learning/meta_orchestrator.py"
echo "BODY: kernel/runtime/ENTRYPOINT.js"
echo "TAG: IMA_KERNEL_PRODUCT_ARCHITECTURE_v1"
