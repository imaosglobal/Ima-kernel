#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[SYNC] pushing changes..."

git add .
git commit -m "auto-sync $(date)" || true
git push origin main

echo "[SYNC] done"
