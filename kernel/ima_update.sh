#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA UPDATE SYNC]"

git pull origin main || true
npm install || true

bash ima_restart.sh

echo "[IMA UPDATE SYNC] done"
