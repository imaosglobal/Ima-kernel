#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL GUARD ==="

LOCK=".ima/runtime/canonical_system_lock.json"

if [ ! -f "$LOCK" ]; then
    echo "[FAIL] lock missing"
    exit 1
fi

echo "[1] VERIFY HASH"

python3 - <<'PY'
import json, hashlib, sys
from pathlib import Path

lock=json.load(open(".ima/runtime/canonical_system_lock.json"))

changed=[]
missing=[]

for f,h in lock["components"].items():
    p=Path(f)
    if not p.exists():
        missing.append(f)
        continue
    now=hashlib.sha256(p.read_bytes()).hexdigest()
    if now != h:
        changed.append(f)

if changed or missing:
    print("[FAIL]")
    print("changed:",changed)
    print("missing:",missing)
    sys.exit(1)

print("[OK] HASH INTEGRITY")
PY


echo "[2] VERIFY MEMORY"

python3 - <<'PY'
from pathlib import Path
import json

checks=[
".ima/runtime/memory_bus.py",
".ima/runtime/memory_fusion_state.json",
".ima/conversation_memory.json"
]

bad=[]

for x in checks:
    if not Path(x).exists():
        bad.append(x)

if bad:
    print("[FAIL] MEMORY",bad)
    raise SystemExit(1)

print("[OK] MEMORY")
PY


echo "[3] VERIFY API"

if curl -s http://127.0.0.1:8080/health | grep -q '"health": "ok"'; then
    echo "[OK] API HEALTH"
else
    echo "[WARN] API OFFLINE"
fi


echo "[4] CREATE CHECKPOINT"

NAME="ima_guard_checkpoint_$(date +%s).tar.gz"

tar -czf "$NAME" \
IMA_START.py \
kernel/runtime/CANONICAL \
.ima/runtime \
ima_master_runtime.py \
conversation_layer.py \
identity_context.py \
learning/evolution_controller.py \
>/dev/null

echo "[OK] BACKUP $NAME"

echo "=== CANONICAL STATE VERIFIED ==="
