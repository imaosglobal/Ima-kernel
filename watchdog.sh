#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

while true
do

RUNNING=$(ps aux | grep "node ima.js" | grep -v grep)

if [ -z "$RUNNING" ]; then
  echo "RESTARTING IMA..."
  nohup node "$ROOT/ima.js" >> "$ROOT/logs/runtime.log" 2>&1 &
fi

sleep 10

done
