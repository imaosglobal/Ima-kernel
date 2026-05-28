#!/data/data/com.termux/files/usr/bin/bash

echo "[FIX] stopping ALL kernels..."

pkill -f server.js || true
pkill -f server_tmp.js || true
pkill -f server_backup_clean.js || true
pkill -f ima_core || true

echo "[FIX] keeping ONLY main server.js"

# remove duplicate auto-starts
sed -i '/IMA KERNEL RUNNING/d' ~/.bashrc 2>/dev/null
sed -i '/server_tmp/d' ~/.bashrc 2>/dev/null
sed -i '/server_backup/d' ~/.bashrc 2>/dev/null

# start ONLY ONE instance
nohup node ~/ima_kernel/server.js > ~/ima_kernel/runtime/logs/server.log 2>&1 &

echo "[FIX] single core running"
