#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"
BRIDGE="$ROOT/bridge_server.js"
LOG="$ROOT/runtime/logs/bridge.log"

mkdir -p $ROOT/runtime/logs

while true
do
  # בדיקה אם bridge רץ
  COUNT=$(ps -ef | grep bridge_server.js | grep -v grep | wc -l)

  if [ "$COUNT" -eq 0 ]; then
    echo "[BRIDGE] restarting $(date)" >> $LOG

    nohup node $BRIDGE >> $LOG 2>&1 &
  fi

  sleep 10
done

