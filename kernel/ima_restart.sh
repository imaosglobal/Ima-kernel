#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA SAFE RESTART]"

pkill -f prod_server.js || true
sleep 2

nohup node ./prod_server.js >> server.log 2>&1 &

sleep 2

curl -s http://localhost:4000/health || echo "[WARN] server not responding"

echo "[IMA SAFE RESTART] done"
