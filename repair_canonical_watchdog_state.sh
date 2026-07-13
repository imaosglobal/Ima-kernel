#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== REPAIR CANONICAL WATCHDOG STATE ==="

mkdir -p kernel/_quarantine_supervisors

for f in \
kernel/experimental/SUPERVISOR.js \
kernel/runtime/KERNEL_SUPERVISOR.js \
kernel/release_freeze/runtime/SUPERVISOR.js
do
    if [ -f "$f" ]; then
        mv "$f" kernel/_quarantine_supervisors/
        echo "[MOVED] $f"
    fi
done


echo ""
echo "=== REBUILD CANONICAL HASHES ==="

python3 - <<'PY'
from pathlib import Path
import hashlib

files=[
"kernel/runtime/CANONICAL/IMA_RUNTIME.js",
"kernel/runtime/CANONICAL/IMA_STATE.js",
"kernel/runtime/CANONICAL/IMA_EVENTS.js",
"kernel/runtime/CANONICAL/IMA_HEAL.js",
"kernel/runtime/CANONICAL/IMA_POLICY.js",
"kernel/runtime/CANONICAL/python_bridge.py",
"kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",
"kernel/runtime/CANONICAL/IMA_WATCHDOG.py",
"IMA_START.py"
]

out=[]

for f in files:
    p=Path(f)
    if p.exists():
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        out.append(f"{f}:{h}")

Path(".ima/governance/CANONICAL_HASHES.txt").write_text(
    "\n".join(out)+"\n"
)

print("[OK] hashes rebuilt")
PY


echo ""
python3 kernel/runtime/CANONICAL/IMA_WATCHDOG.py
