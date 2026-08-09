#!/data/data/com.termux/files/usr/bin/bash

BASE=~/ima_os
PID_FILE="$BASE/state/control_plane.pid"
REG_FILE="$BASE/state/process_registry.json"
LOG="$BASE/logs/control_plane.log"
API="http://127.0.0.1:3000"
UI_DIR=~/ima_kernel/ima-ui

mkdir -p "$BASE/state" "$BASE/logs" "$BASE/bridge"

# ----------------------------
# SINGLETON LOCK
# ----------------------------
if [ -f "$PID_FILE" ]; then
  OLD_PID=$(cat "$PID_FILE")
  if ps -p "$OLD_PID" >/dev/null 2>&1; then
    echo "[CONTROL] already running PID=$OLD_PID"
    exit 0
  fi
fi

echo $$ > "$PID_FILE"
echo "[CONTROL] boot PID=$$" | tee -a "$LOG"

# ----------------------------
# CORE FUNCTIONS
# ----------------------------
register() {
  NAME=$1
  PID=$2
  echo "{\"name\":\"$NAME\",\"pid\":$PID,\"time\":\"$(date -Iseconds)\"}" >> "$REG_FILE"
}

start_backend() {
  pgrep -f "server.js" >/dev/null && return
  echo "[CONTROL] starting backend" | tee -a "$LOG"
  nohup node ~/ima_kernel/server.js >> "$BASE/logs/backend.log" 2>&1 &
  register "backend" "$!"
}

start_ui() {
  pgrep -f "vite" >/dev/null && return
  echo "[CONTROL] starting UI" | tee -a "$LOG"
  nohup npm --prefix "$UI_DIR" run dev -- --host 0.0.0.0 >> "$BASE/logs/ui.log" 2>&1 &
  register "ui" "$!"
}

bridge_loop() {
  mkdir -p "$BASE/bridge"

  IN="$BASE/bridge/in.txt"
  OUT="$BASE/bridge/out.txt"
  LOCK="$BASE/bridge/lock"

  # atomic read using flock
  {
    flock 200

    MSG=$(cat "$IN" 2>/dev/null)

    if [ -n "$MSG" ]; then
      echo "[BRIDGE] recv: $MSG" | tee -a "$LOG"
      echo "ACK: $MSG @ $(date -Iseconds)" >> "$OUT"
      : > "$IN"
    fi

  } 200>"$LOCK"
}

health_check() {
  curl -fsS "$API/health" >/dev/null 2>&1
}

watchdog() {
  health_check || start_backend
  pgrep -f "vite" >/dev/null || start_ui
}

echo "[CONTROL] system online" | tee -a "$LOG"

start_backend
start_ui

while true; do
  watchdog
  bridge_loop
  sleep 2
done
