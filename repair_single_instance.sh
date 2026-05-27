#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

echo "[FIX] stopping all kernel processes"
pkill -f server.js || true
pkill -f watchdog.sh || true

sleep 2

echo "[FIX] enforcing single instance"
cd "$ROOT"

nohup node server.js > runtime/logs/server.log 2>&1 &
nohup bash watchdog.sh > runtime/logs/watchdog.log 2>&1 &

echo "[FIX] status check"
pgrep -af server.js
curl -s http://127.0.0.1:3000/health || echo "server down"

echo "[DONE]"
