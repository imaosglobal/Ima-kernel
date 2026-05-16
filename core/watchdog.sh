#!/data/data/com.termux/files/usr/bin/bash

while true; do
  curl -s localhost:3000/health >/dev/null
  if [ $? -ne 0 ]; then
    echo "[WATCHDOG] restart kernel"
    pkill -f node
    cd ~/ima_kernel && ./scripts/start.sh
  fi
  sleep 10
done
