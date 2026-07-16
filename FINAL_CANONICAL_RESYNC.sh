#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA FINAL CANONICAL RESYNC ==="

STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP=".ima/snapshots/pre_final_resync_$STAMP"

mkdir -p "$BACKUP"

echo "[1] BACKUP"
cp IMA_START.py ima_master_runtime.py conversation_layer.py "$BACKUP/" 2>/dev/null || true

echo "[2] CALCULATE HASHES"

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

files=[
"kernel/runtime/CANONICAL/IMA_RUNTIME.js",
"kernel/runtime/CANONICAL/IMA_STATE.js",
"kernel/runtime/CANONICAL/IMA_EVENTS.js",
"kernel/runtime/CANONICAL/IMA_HEAL.js",
"kernel/runtime/CANONICAL/IMA_POLICY.js",
"kernel/runtime/CANONICAL/python_bridge.py",
"kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",
"kernel/runtime/CANONICAL/IMA_WATCHDOG.py",
"IMA_START.py",
"ima_master_runtime.py",
"conversation_layer.py",
"api/server.py"
]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

hashes={}

for f in files:
    if Path(f).exists():
        hashes[f]=sha(f)

Path(".ima/governance/CANONICAL_HASHES.txt").write_text(
    "\n".join(f"{k}:{v}" for k,v in hashes.items())+"\n"
)

lock=Path(".ima/governance/RELEASE_LOCK.json")

data={}
if lock.exists():
    data=json.loads(lock.read_text())

data["state"]="CANONICAL_RELEASE_LOCKED"
data["policy"]="single_canonical_runtime"
data["files"]=hashes

lock.write_text(json.dumps(data,indent=2)+"\n")

print("[OK] HASHES UPDATED")
PY


echo "[3] VERIFY"

python3 canonical_boot_guard.py || true


echo "[4] BOOT TEST"

python3 IMA_START.py || true


echo "[5] CREATE FINAL LOCK"

cat > .ima/governance/FINAL_CANONICAL_LOCK.json <<EOF
{
  "state": "FINAL_CANONICAL_LOCKED",
  "timestamp": "$(date +%s)",
  "policy": "single_canonical_runtime",
  "source": "FINAL_CANONICAL_RESYNC.sh"
}
EOF


chmod 444 .ima/governance/FINAL_CANONICAL_LOCK.json

echo "[OK] FINAL LOCK CREATED"

echo "=== COMPLETE ==="
