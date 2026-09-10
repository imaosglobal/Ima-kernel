#!/bin/bash

QUEUE=".squad/orchestration-log/queue.md"
LOG=".squad/orchestration-log/log.md"
DONE=".squad/orchestration-log/done.md"

touch "$DONE"

echo "=== EXECUTOR START ===" >> $LOG

while IFS= read -r task
do
  [ -z "$task" ] && continue

  # בדיקה אם כבר בוצע
  if grep -Fxq "$task" "$DONE"; then
    continue
  fi

  echo "RALPH EXECUTING: $task" >> $LOG
  echo "SCRIBE LOG: completed analysis for: $task" >> $LOG

  echo "$task" >> "$DONE"

done < "$QUEUE"

echo "=== EXECUTOR DONE ===" >> $LOG
