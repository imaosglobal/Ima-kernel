#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

echo "[IMA MODE] booting clean stack..."

# start kernel
nohup node server.js > runtime/logs/server.log 2>&1 &

# start watchdog
nohup bash watchdog.sh > runtime/logs/watchdog.log 2>&1 &

sleep 2

echo "[IMA MODE] health:"
curl -s http://127.0.0.1:3000/health || echo "DOWN"

echo "[IMA MODE] status:"
pgrep -af server.js
pgrep -af watchdog.sh

echo "[IMA MODE] ready"
