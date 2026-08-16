#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
RUNTIME="$ROOT/.ima/ORCHESTRATION/runtime"

ENGINE="$RUNTIME/automatic_cycle_engine.py"
PIDFILE="$RUNTIME/automatic_cycles.pid"
LOG="$RUNTIME/automatic_cycles.log"

if [ -f "$PIDFILE" ]; then
    PID="$(cat "$PIDFILE" 2>/dev/null || true)"
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "[OK] automatic cycle engine already running: PID $PID"
        exit 0
    fi
fi

nohup python "$ENGINE" >> "$LOG" 2>&1 &
PID=$!

echo "$PID" > "$PIDFILE"

sleep 3

if kill -0 "$PID" 2>/dev/null; then
    echo "[OK] automatic cycle engine started"
    echo "[OK] PID: $PID"
else
    echo "[FAIL] automatic cycle engine exited"
    tail -100 "$LOG" || true
    exit 1
fi
