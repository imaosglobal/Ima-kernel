#!/data/data/com.termux/files/usr/bin/bash

BASE=~/ima_os
BRIDGE_IN="$BASE/bridge/in.txt"
BRIDGE_OUT="$BASE/bridge/out.txt"
LOG="$BASE/logs/kernel.log"
STATE="$BASE/state/state.json"

mkdir -p "$BASE/bridge" "$BASE/logs" "$BASE/state"

echo "[KERNEL] booting..." >> "$LOG"

while true; do

  # ===== EVENT LOOP =====
  if [ -f "$BRIDGE_IN" ]; then
    MSG=$(cat "$BRIDGE_IN")

    if [ ! -z "$MSG" ]; then
      echo "[EVENT] $MSG" >> "$LOG"

      echo "{\"type\":\"ack\",\"msg\":\"$MSG\",\"time\":\"$(date -Iseconds)\"}" >> "$BRIDGE_OUT"

      echo "" > "$BRIDGE_IN"
    fi
  fi

  # ===== HEALTH SNAPSHOT =====
  echo "{\"time\":\"$(date -Iseconds)\",\"status\":\"alive\"}" > "$STATE/state.json"

  sleep 2
done
