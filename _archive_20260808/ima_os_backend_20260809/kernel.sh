#!/data/data/com.termux/files/usr/bin/bash

BASE=~/ima_os
LOG="$BASE/logs/kernel.log"
BUS_INBOX="$BASE/bus/inbox.log"

mkdir -p "$BASE/logs" "$BASE/bus"

declare -A PIDS
declare -A CMDS

log() {
  echo "[KERNEL] $1" | tee -a "$LOG"
}

emit() {
  echo "$1" >> "$BUS_INBOX"
}

start_service() {
  NAME="$1"
  CMD="$2"

  # prevent duplicate
  if [[ -n "${PIDS[$NAME]}" ]] && kill -0 "${PIDS[$NAME]}" 2>/dev/null; then
    log "skip start $NAME"
    return
  fi

  log "starting $NAME"

  nohup bash -c "$CMD" >> "$BASE/logs/${NAME}.log" 2>&1 &
  PID=$!

  PIDS[$NAME]=$PID
  CMDS[$NAME]="$CMD"

  emit "{\"type\":\"service.started\",\"name\":\"$NAME\",\"pid\":$PID}"
}

restart_service() {
  NAME="$1"

  log "restarting $NAME"

  if [[ -n "${PIDS[$NAME]}" ]]; then
    kill "${PIDS[$NAME]}" 2>/dev/null
  fi

  start_service "$NAME" "${CMDS[$NAME]}"
}

watchdog() {
  curl -fsS http://127.0.0.1:3000/health >/dev/null 2>&1 || {
    start_service backend "node ~/ima_kernel/server.js"
  }

  pgrep -f vite >/dev/null || {
    start_service ui "npm --prefix ~/ima_kernel/ima-ui run dev -- --host 0.0.0.0"
  }
}

event_loop() {
  log "event loop started"

  tail -F "$BUS_INBOX" | while read -r event; do

    TYPE=$(echo "$event" | grep -o '"type":"[^"]*"' | cut -d':' -f2 | tr -d '"')
    NAME=$(echo "$event" | grep -o '"name":"[^"]*"' | cut -d':' -f2 | tr -d '"')

    case "$TYPE" in
      service.crash)
        log "crash detected: $NAME"
        restart_service "$NAME"
        ;;
      service.restart)
        restart_service "$NAME"
        ;;
    esac

  done
}

log "booting kernel"

start_service backend "node ~/ima_kernel/server.js"
start_service ui "npm --prefix ~/ima_kernel/ima-ui run dev -- --host 0.0.0.0"

event_loop &

while true; do
  watchdog
  sleep 2
done
