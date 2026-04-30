#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA UPDATE] pulling latest from git..."
git pull origin main || true

echo "[IMA UPDATE] installing dependencies..."
npm install || true

echo "[IMA UPDATE] restarting runtime..."

pkill -f prod_server.js || true
pkill -f watchdog.sh || true

nohup node prod_server.js > server.log 2>&1 &
nohup bash ~/ima_core/kernel/watchdog.sh > watchdog.log 2>&1 &

echo "[IMA UPDATE] health check..."
sleep 2

curl -s http://localhost:4000/health || echo "[WARN] health failed"

echo "[IMA UPDATE] done"
