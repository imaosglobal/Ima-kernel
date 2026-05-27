#!/data/data/com.termux/files/usr/bin/bash

LOCK=/data/data/com.termux/files/home/ima_kernel/runtime/.lock

if [ -f "$LOCK" ] && pgrep -f server.js > /dev/null; then
  exit 0
fi

echo $$ > "$LOCK"

nohup node ~/ima_kernel/server.js >> ~/ima_kernel/runtime/logs/server.log 2>&1 &
nohup bash ~/ima_kernel/watchdog.sh >> ~/ima_kernel/runtime/logs/watchdog.log 2>&1 &
