#!/data/data/com.termux/files/usr/bin/bash

LOG=~/ima_core/kernel/server.log

echo "[EXEC] stopping server..."
pkill -f prod_server.js || true
sleep 2

echo "[EXEC] starting server..."
cd ~/ima_core/kernel

nohup node prod_server.js >> $LOG 2>&1 &
PID=$!

sleep 2

# verify
curl -s http://localhost:4000/health >/dev/null && {
  echo "[EXEC] restart OK"
  echo "[EXEC] PID: $PID"
} || {
  echo "[EXEC] restart FAILED"
}

echo "[EXEC] restart done"
