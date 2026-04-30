#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA BOOT] syncing with git..."
git pull origin main || true

echo "[IMA BOOT] installing dependencies..."
npm install || true

echo "[IMA BOOT] stopping old processes..."
pkill -f prod_server.js || true
pkill -f watchdog.sh || true

echo "[IMA BOOT] starting server..."
nohup node prod_server.js > server.log 2>&1 &

echo "[IMA BOOT] starting watchdog (stable)..."
nohup bash ~/ima_core/kernel/watchdog.sh > watchdog.log 2>&1 &

echo "[IMA BOOT] system ready"
