#!/data/data/com.termux/files/usr/bin/bash

echo "[STABILIZE] stopping all duplicates..."

pkill -f node || true
pkill -f server.js || true
pkill -f watchdog.sh || true

echo "[STABILIZE] clearing auto-start chaos..."

sed -i '/ima_kernel/d' ~/.bashrc
sed -i '/server.js/d' ~/.bashrc
sed -i '/watchdog/d' ~/.bashrc

echo "[STABILIZE] starting single server..."

nohup node ~/ima_kernel/server.js > ~/ima_kernel/runtime/logs/server.log 2>&1 &

sleep 2

echo "[STABILIZE] health:"
curl -s http://127.0.0.1:3000/health || echo "DOWN"

echo "[STABILIZE] active processes:"
pgrep -af server.js || echo "NO SERVER"

echo "[DONE] stable state achieved"
