#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

echo "=== IMA STATUS ==="

echo "[PROCESS]"
ps -ef | grep ima_daemon | grep -v grep || echo "daemon missing"

echo
echo "[LOCK]"
ls -la .ima/*daemon* 2>/dev/null || echo "no daemon lock"

echo
echo "[STATE]"
python3 - <<'PY'
from ima_kernel import load_events
try:
    from ima_reducer import reduce
    print(reduce(load_events()))
except Exception as e:
    print("ERROR:",e)
PY

echo
echo "[LOG]"
tail -20 nohup.out 2>/dev/null || echo "no log"

