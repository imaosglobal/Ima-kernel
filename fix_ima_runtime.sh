#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA RUNTIME REPAIR ==="

cd ~/ima_kernel

echo "[1] Searching IMA processes..."
ps -ef | grep -E "ima|python" | grep -v grep || true

echo "[2] Killing stale daemon processes..."
pkill -f "ima_daemon.py" || true
pkill -f "kernel.run" || true

sleep 2

echo "[3] Finding lock files..."
find . -maxdepth 3 -type f \( -name "*.lock" -o -name "*.pid" \) -print

echo "[4] Removing stale locks..."
find . -maxdepth 3 -type f \( -name "*.lock" -o -name "*.pid" \) -delete || true

echo "[5] Searching heartbeat sources..."
grep -R "heartbeat\|LIVE KERNEL\|STATE UPDATE" -n . \
 --exclude-dir=.git \
 --exclude-dir=.ima \
 --exclude="nohup.old.out" \
 || true

echo "[6] Backing old log..."
if [ -f nohup.out ]; then
    mv nohup.out nohup.backup.$(date +%s).out
fi

echo "[7] Starting daemon..."
nohup python3 ima_daemon.py > nohup.out 2>&1 &

sleep 3

echo "[8] New daemon log:"
cat nohup.out

echo "[9] Checking kernel state..."

python3 - <<'PY'
from ima_kernel import load_events
import sys

sys.path.insert(0,'.ima')

try:
    from ima_reducer import reduce
    state = reduce(load_events())
except Exception as e:
PY

echo "[10] Git status:"
git status --short

echo "=== REPAIR COMPLETE ==="
