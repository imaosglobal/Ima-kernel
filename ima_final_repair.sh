#!/data/data/com.termux/files/usr/bin/bash

set -e

cd ~/ima_kernel

echo "=== IMA FINAL REPAIR ==="

echo "[1] Stop old processes"
pkill -f "ima_daemon.py" || true
sleep 2

echo "[2] Remove stale runtime locks"
find .ima -type f \( -name "*.lock" -o -name "*.pid" \) -delete 2>/dev/null || true

echo "[3] Backup logs"
mkdir -p backup_logs
cp -f nohup.out backup_logs/ 2>/dev/null || true
cp -f .ima/daemon.* backup_logs/ 2>/dev/null || true

echo "[4] Verify no heartbeat kernel source exists"
grep -R "heartbeat\|LIVE KERNEL STARTED\|\[ACTION\]" \
. --include="*.py" --exclude-dir=.git --exclude-dir=.ima || true

echo "[5] Check imports"
python3 - <<'PY'
import ima_system
import ima_daemon
PY

echo "[6] Start clean daemon"
nohup python3 ima_daemon.py > .ima/daemon.out 2>&1 &

sleep 3

echo "[7] Process"
ps -ef | grep ima_daemon | grep -v grep || true

echo "[8] State"
python3 - <<'PY'
from ima_kernel import load_events
from ima_reducer import reduce
PY

echo "[9] Test query"
python3 ima.py ask "hello"

echo "=== DONE ==="
