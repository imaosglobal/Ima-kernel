#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL ARCHITECTURE FINALIZER ==="

mkdir -p .ima/governance

STAMP=$(date +%s)

echo "[1] Creating safety snapshot"

git status > ".ima/governance/pre_canonical_status_$STAMP.txt" || true


echo "[2] Creating canonical map"

cat > .ima/governance/canonical_architecture.json <<EOF
{
  "system":"IMA",
  "state":"LOCKED",

  "brain":
  "learning/meta_orchestrator.py",

  "runtime":
  "kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",

  "event_bus":
  "kernel/runtime/KERNEL_EVENT_BUS.js",

  "api":
  "kernel/runtime/KERNEL_API_GATEWAY.js",

  "scheduler":
  "learning/safe_scheduler.py",

  "device_layer":
  "kernel/device",

  "plugins":
  "kernel/plugins",

  "persona":
  "learning/persona_engine.py",

  "child_safety":
  "learning/child_safety_engine.py",

  "policy":[
    "single_brain_only",
    "single_runtime_only",
    "single_event_bus_only",
    "single_api_gateway_only",
    "block_duplicate_creation",
    "redirect_to_canonical"
  ],

  "locked_at":$STAMP
}
EOF


echo "[3] Creating duplicate protection"

cat > learning/canonical_guard.py <<'PY'
from pathlib import Path
import json

REGISTRY=Path(".ima/governance/canonical_architecture.json")

def canonical():
    return json.loads(
        REGISTRY.read_text()
    )

def verify(component,path):

    data=canonical()

    allowed=data.get(component)

    if allowed and str(path)!=allowed:

        raise RuntimeError(
            "\nIMA BLOCKED DUPLICATE COMPONENT\n"
            f"Component: {component}\n"
            f"Use canonical path:\n{allowed}\n"
        )

    return True


if __name__=="__main__":
PY


echo "[4] Checking canonical components"

python3 - <<'PY'
from pathlib import Path
import json

data=json.loads(
Path(".ima/governance/canonical_architecture.json").read_text()
)

for name,path in data.items():
    if isinstance(path,str) and (
        path.endswith(".py") or
        path.endswith(".js")
    ):
            name,
            "OK" if Path(path).exists()
            else "MISSING",
            path
        )
PY


echo "[5] Writing architecture status"

python3 - <<'PY'
from pathlib import Path
import json,time

r={
"time":time.time(),
"system":"IMA",
"state":"CANONICAL_LOCKED",
"registry":".ima/governance/canonical_architecture.json"
}

Path(".ima/governance/canonical_status.json").write_text(
json.dumps(r,indent=2),
encoding="utf-8"
)

PY


echo "[6] Commit"

git add \
.ima/governance/canonical_architecture.json \
.ima/governance/canonical_status.json \
learning/canonical_guard.py

git commit -m "IMA canonical architecture locked"

git tag -a IMA_CANONICAL_ARCHITECTURE_LOCKED_v1 \
-m "IMA single canonical architecture locked" || true


echo "=== IMA CANONICAL LOCK COMPLETE ==="
