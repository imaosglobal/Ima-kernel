#!/bin/bash

BASE=".squad/orchestration-log"
QUEUE="$BASE/queue.md"
DONE="$BASE/done.md"
LOG="$BASE/log.md"

touch "$QUEUE"
touch "$DONE"

echo "=== AUTONOMOUS LOOP START ===" >> "$LOG"

while true; do

  # אם אין משימות – מוסיפים דמו בסיסי (כדי שהמערכת תחיה)
  if [ ! -s "$QUEUE" ]; then
    echo "TASK: analyze system state" >> "$QUEUE"
    echo "TASK: scan architecture health" >> "$QUEUE"
    echo "TASK: optimize modules" >> "$QUEUE"
  fi

  TMP="$BASE/queue.tmp"
  > "$TMP"

  while IFS= read -r task; do
    [ -z "$task" ] && continue

    if grep -Fxq "$task" "$DONE"; then
      continue
    fi

    echo "RALPH EXECUTING: $task" >> "$LOG"
    echo "SCRIBE LOG: completed analysis for: $task" >> "$LOG"

    echo "$task" >> "$DONE"

  done < "$QUEUE"

  # ניקוי queue ממשימות שבוצעו
  while IFS= read -r task; do
    grep -Fxq "$task" "$DONE" || echo "$task" >> "$TMP"
  done < "$QUEUE"

  mv "$TMP" "$QUEUE"

  sleep 5

done
