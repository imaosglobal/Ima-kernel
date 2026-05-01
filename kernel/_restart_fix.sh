#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA PID RESTART]"

if [ -f server.pid ]; then
  kill -9 $(cat server.pid) 2>/dev/null || true
  rm -f server.pid
fi

pkill -9 -f prod_server.js 2>/dev/null || true

sleep 1

nohup bash _server_runner.sh > server.log 2>&1 &

echo "[IMA PID RESTART DONE]"
