#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA WORKER STARTED]"

while true; do

  TASKS=$(cat tasks.db.json 2>/dev/null)

  if echo "$TASKS" | grep -q "pending"; then
    echo "[WORKER] processing tasks..."
  fi

  sleep 10
done
