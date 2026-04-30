#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA BOOT SYNC] pulling latest..."
git pull origin main || true

echo "[IMA BOOT SYNC] installing..."
npm install || true

echo "[IMA BOOT SYNC] starting server..."

pkill -f prod_server.js || true
sleep 2

nohup node prod_server.js > server.log 2>&1 &

echo "[IMA BOOT SYNC] done"
