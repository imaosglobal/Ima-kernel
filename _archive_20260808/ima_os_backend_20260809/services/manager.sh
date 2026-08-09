#!/data/data/com.termux/files/usr/bin/bash

BASE=~/ima_os
API="http://127.0.0.1:3000"

start_backend() {
  curl -fsS "$API/health" >/dev/null 2>&1 && return

  echo "[SERVICE] starting backend" >> "$BASE/logs/services.log"
  nohup node ~/ima_kernel/server.js >> "$BASE/logs/backend.log" 2>&1 &
}

start_ui() {
  pgrep -f vite >/dev/null 2>&1 && return

  echo "[SERVICE] starting UI" >> "$BASE/logs/services.log"
  nohup npm --prefix ~/ima_kernel/ima-ui run dev -- --host 0.0.0.0 >> "$BASE/logs/ui.log" 2>&1 &
}

while true; do
  start_backend
  start_ui
  sleep 5
done
