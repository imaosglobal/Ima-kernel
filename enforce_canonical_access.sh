#!/data/data/com.termux/files/usr/bin/bash
set -e

R=.ima/agi_evolution/runtime
LOCK="$R/CANONICAL_KERNEL_LOCK.json"

echo "=== CANONICAL ACCESS CHECK ==="

if [ ! -f "$LOCK" ]; then
  echo "[FAIL] Missing canonical lock"
  exit 1
fi

KERNEL=$(python3 - <<'PY'
import json
p=".ima/agi_evolution/runtime/CANONICAL_KERNEL_LOCK.json"
PY
)

HANDOFF=$(python3 - <<'PY'
import json
p=".ima/agi_evolution/runtime/CANONICAL_KERNEL_LOCK.json"
PY
)

echo "LOCKED KERNEL: $KERNEL"
echo "LOCKED HANDOFF: $HANDOFF"

if [ "$KERNEL" != "kernel/runtime/CANONICAL/python_bridge.py" ]; then
  echo "[FAIL] Wrong kernel"
  exit 1
fi

if [ "$HANDOFF" != "ima_master_runtime" ]; then
  echo "[FAIL] Wrong handoff"
  exit 1
fi

echo "[OK] All access must route through canonical kernel"
echo "=== CANONICAL ACCESS ENFORCED ==="
