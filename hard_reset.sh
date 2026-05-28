#!/data/data/com.termux/files/usr/bin/bash

echo "[HARD RESET] killing ALL node/kernel processes..."

# kill EVERYTHING related
pkill -f node || true
pkill -f server.js || true
pkill -f watchdog.sh || true
pkill -f ima_kernel || true

echo "[HARD RESET] cleaning duplicate boot entries..."

# remove ALL auto-start hooks
sed -i '/ima_kernel/d' ~/.bashrc
sed -i '/server.js/d' ~/.bashrc
sed -i '/IMA KERNEL RUNNING/d' ~/.bashrc
sed -i '/watchdog/d' ~/.bashrc

echo "[HARD RESET] clearing runtime logs..."
rm -f ~/ima_kernel/runtime/logs/*.log

echo "[HARD RESET] starting SINGLE clean instance..."

nohup node ~/ima_kernel/server.js > ~/ima_kernel/runtime/logs/server.log 2>&1 &

sleep 2

echo "[HARD RESET] check:"
pgrep -af server.js || echo "NO SERVER RUNNING"

echo "[DONE] system reset complete"
