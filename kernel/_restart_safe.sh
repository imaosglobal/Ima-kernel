#!/data/data/com.termux/files/usr/bin/bash

echo "[IMA SAFE RESTART] starting..."

pkill -f prod_server.js || true
sleep 2

cd ~/ima_core/kernel

nohup node prod_server.js > server.log 2>&1 &

echo "[IMA SAFE RESTART] done"
