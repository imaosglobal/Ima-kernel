#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

LOG="$ROOT/runtime/logs/guardian.log"

mkdir -p $ROOT/runtime/logs

echo "" >> $LOG
echo "GUARDIAN START => $(date)" >> $LOG

while true
do

SERVER_COUNT=$(ps -ef | grep node | grep server.js | grep -v grep | wc -l)

WATCHDOG_COUNT=$(ps -ef | grep watchdog.sh | grep -v grep | wc -l)

DISK=$(df $HOME | tail -1 | awk '{print $5}' | sed 's/%//')

LAST_HEARTBEAT_FILE="$ROOT/runtime/state/heartbeat.txt"

RUN_GUARD=0

if [ "$SERVER_COUNT" -ne 1 ]; then
  RUN_GUARD=1
fi

if [ "$WATCHDOG_COUNT" -ne 1 ]; then
  RUN_GUARD=1
fi

if [ "$DISK" -gt 90 ]; then
  RUN_GUARD=1
fi

if [ ! -f "$LAST_HEARTBEAT_FILE" ]; then
  RUN_GUARD=1
else

LAST=$(stat -c %Y "$LAST_HEARTBEAT_FILE")
NOW=$(date +%s)

DIFF=$((NOW-LAST))

if [ "$DIFF" -gt 900 ]; then
  RUN_GUARD=1
fi

fi

if [ "$RUN_GUARD" -eq 1 ]; then

  echo "GUARD RUN => $(date)" >> $LOG

  bash $ROOT/system_guard.sh \
  >> $LOG 2>&1

fi

sleep 300

done
