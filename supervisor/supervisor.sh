#!/bin/bash

ROOT="$HOME/ima_kernel"
LOG="$ROOT/runtime/logs/supervisor.log"

mkdir -p "$ROOT/runtime/logs"

while true; do
  # check only once, no respawn storms
  if ! pgrep -f ima_pro_saas >/dev/null; then
    echo "[SUPERVISOR] starting ima_pro_saas" >> "$LOG"
    node "$ROOT/kernel/ima_pro_saas.js" >> "$LOG" 2>&1 &
  fi

  if ! pgrep -f prod_server >/dev/null; then
    echo "[SUPERVISOR] starting prod_server" >> "$LOG"
    node "$ROOT/kernel/prod_server.js" >> "$LOG" 2>&1 &
  fi

  sleep 15
done
