#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA RELEASE] syncing git..."

git add .
git commit -m "auto release $(date)" || true
git push origin main || true

echo "[IMA RELEASE] version bump..."
npm version patch --no-git-tag-version || true

echo "[IMA RELEASE] updating dependencies..."
npm install

echo "[IMA RELEASE] restarting runtime..."
pkill -f prod_server.js || true
nohup node prod_server.js > server.log 2>&1 &

echo "[IMA RELEASE] syncing termux boot..."
cp ~/.bashrc ~/.bashrc.backup || true

echo "[IMA RELEASE] done"
