#!/data/data/com.termux/files/usr/bin/bash

LOG=/data/data/com.termux/files/home/ima_core/kernel/server.log

echo "[EXEC] stopping server..."
pkill -f prod_server.js || true
sleep 2

echo "[EXEC] starting server..."
cd /data/data/com.termux/files/home/ima_core/kernel

nohup node prod_server.js >> $LOG 2>&1 &

echo "[EXEC] restart done"
