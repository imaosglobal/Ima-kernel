#!/data/data/com.termux/files/usr/bin/bash

while true; do
  if ! pgrep -f "server.js" > /dev/null; then
    echo "[WATCHDOG] restart $(date)" >> ~/ima_kernel/runtime/logs/watchdog.log
    nohup node ~/ima_kernel/server.js >> ~/ima_kernel/runtime/logs/server.log 2>&1 &
  fi
  sleep 5
done
bash ~/ima_kernel/kernel/memory_engine_v2.sh
