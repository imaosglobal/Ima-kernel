#!/bin/bash

BASE=".squad/orchestration-log"
BRAIN=".squad/brain"
QUEUE="$BASE/queue.md"
DONE="$BASE/done.md"
LOG="$BASE/log.md"
MEM="$BRAIN/memory.md"

touch "$QUEUE" "$DONE" "$LOG" "$MEM"

echo "=== SUPER AUTONOMOUS START ===" >> "$LOG"

while true; do

  # ===== PLANNER (RALPH SIMULATION) =====
  LAST_DONE=$(tail -n 3 "$DONE")

  if [ -z "$LAST_DONE" ]; then
    echo "TASK: initialize system scan" >> "$QUEUE"
    echo "TASK: map architecture baseline" >> "$QUEUE"
  else
    # יצירת משימות לפי מצב
    echo "TASK: optimize last execution cycle" >> "$QUEUE"
  fi

  # ===== EXECUTION =====
  TMP="$BASE/queue.tmp"
  > "$TMP"

  while IFS= read -r task; do
    [ -z "$task" ] && continue

    # מניעת כפילויות
    if grep -Fxq "$task" "$DONE"; then
      continue
    fi

    echo "RALPH THINKS: $task" >> "$LOG"
    echo "SCRIBE RECORDS: $task" >> "$LOG"

    echo "$task" >> "$DONE"
    echo "$task executed at $(date)" >> "$MEM"

  done < "$QUEUE"

  # ניקוי queue
  while IFS= read -r task; do
    grep -Fxq "$task" "$DONE" || echo "$task" >> "$TMP"
  done < "$QUEUE"

  mv "$TMP" "$QUEUE"

  # ===== STABILIZER =====
  # מונע הצפה
  tail -n 50 "$QUEUE" > "$QUEUE.tmp" && mv "$QUEUE.tmp" "$QUEUE"

  sleep 5

done
