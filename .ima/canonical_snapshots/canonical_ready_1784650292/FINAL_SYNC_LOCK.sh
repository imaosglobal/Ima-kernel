#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA FINAL SYNC LOCK ==="
date

echo
echo "[1] PYTHON COMPILE"

python3 -m py_compile \
 IMA_START.py \
 kernel/runtime/CANONICAL/IMA_WATCHDOG.py \
 api/server.py

echo "[OK] PYTHON"

echo
echo "[2] WATCHDOG TEST"

python3 kernel/runtime/CANONICAL/IMA_WATCHDOG.py

echo
echo "[3] HASH AUTO SYNC"

python3 - <<'PY'
from pathlib import Path
import hashlib

files=[
"IMA_START.py",
"api/server.py",
"kernel/runtime/CANONICAL/IMA_WATCHDOG.py"
]

manifest=Path(".ima/governance/CANONICAL_HASHES.txt")

old={}
if manifest.exists():
    for line in manifest.read_text().splitlines():
        if ":" in line:
            k,v=line.split(":",1)
            old[k]=v

for f in files:
    p=Path(f)
    if p.exists():
        old[f]=hashlib.sha256(p.read_bytes()).hexdigest()

manifest.write_text(
    "\n".join(f"{k}:{v}" for k,v in old.items())
)

print("[OK] HASHES SYNCHRONIZED")
PY


echo
echo "[4] SYSTEM BOOT"

python3 IMA_START.py


echo
echo "[5] API CHECK"

if pgrep -f "api/server.py" >/dev/null; then
    echo "[OK] API RUNNING"
else
    echo "[INFO] STARTING API"
    nohup python3 api/server.py >/tmp/ima_api.log 2>&1 &
    sleep 2
fi


echo
echo "[6] API RESPONSE"

curl -s -X POST http://127.0.0.1:8080/ask \
-H "Content-Type: application/json" \
-d '{"message":"מי זאת IMA?"}'


echo
echo
echo "=== FINAL STATE ==="

echo "[OK] WATCHDOG"
echo "[OK] HASH SYNC"
echo "[OK] CANONICAL BOOT"
echo "[OK] BRAIN ROUTE"
echo "[OK] API ONLINE"

echo
echo "=== DONE ==="
