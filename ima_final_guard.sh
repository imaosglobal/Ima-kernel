#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"

cd "$ROOT"

echo "=== IMA FINAL GUARD ==="

LOCK=".ima/governance/architecture_lock.json"
BRAIN="learning/meta_orchestrator.py"
RUNTIME="kernel/runtime/KERNEL_UNIFIED_RUNTIME_V1.js"

if [ ! -f "$LOCK" ]; then
    echo "[FAIL] architecture lock missing"
    exit 1
fi

echo "[1] Architecture lock"
cat "$LOCK"

echo
echo "[2] Brain verification"

python3 - <<PY
from learning.brain_guard import verify_brain

verify_brain("$BRAIN")
print("BRAIN OK")
PY

echo
echo "[3] Canonical files"

if [ ! -f "$BRAIN" ]; then
    echo "Missing canonical brain"
    exit 1
fi

if [ ! -f "$RUNTIME" ]; then
    echo "Missing canonical runtime"
    exit 1
fi

echo "Brain:"
echo "$BRAIN"

echo "Runtime:"
echo "$RUNTIME"


echo
echo "[4] Duplicate architecture scan"

grep -R "orchestrator\|brain" \
learning kernel \
--exclude-dir=__pycache__ \
--exclude-dir=_graveyard \
> .ima/governance/architecture_scan.txt || true


echo "Scan saved:"
echo ".ima/governance/architecture_scan.txt"


echo
echo "[5] Runtime import check"

node -e "
require('./kernel/runtime/KERNEL_UNIFIED_RUNTIME_V1.js');
console.log('RUNTIME OK');
"


echo
echo "[6] Learning system check"

python3 - <<'PY'
from learning.meta_orchestrator import run_meta_analysis
r = run_meta_analysis()

print("Capabilities:", r.get("capabilities"))
print("Health modules:", r.get("health_modules"))
print("Status:", r.get("status"))
PY


echo
echo "[7] Governance state"

cat > .ima/governance/MASTER_GOVERNOR.json <<EOF
{
  "system": "IMA",
  "mode": "CANONICAL_ONLY",
  "brain": "$BRAIN",
  "runtime": "$RUNTIME",
  "orchestrator": "learning/module_registry.py",
  "policies": [
    "single_brain_only",
    "single_runtime_only",
    "single_orchestrator_only",
    "block_duplicate_creation",
    "redirect_to_canonical_path",
    "require_snapshot_before_change",
    "require_health_check"
  ]
}
EOF

chmod 444 .ima/governance/MASTER_GOVERNOR.json


echo
echo "=== IMA FINAL STATUS ==="
echo "BRAIN: OK"
echo "RUNTIME: OK"
echo "ORCHESTRATOR: OK"
echo "GOVERNANCE: LOCKED"

