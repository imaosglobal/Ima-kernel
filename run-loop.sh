#!/bin/bash

QUEUE=".squad/orchestration-log/queue.md"

echo "=== LOOP START ==="

while true; do

  echo ""
  echo "cycle start"

  # יצירת events
  bash .squad/intelligence/event-generator.sh

  echo ""
  echo "--- QUEUE SNAPSHOT ---"
  cat "$QUEUE"

  echo ""
  echo "cycle done"
  echo "----------------------"

  sleep 3

done
