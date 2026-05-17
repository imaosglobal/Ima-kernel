#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

cd "$ROOT"

LOCK="$ROOT/runtime/kernel.lock"

if [ -f "$LOCK" ]; then
  PID=$(cat "$LOCK" 2>/dev/null || true)

  if ps -p "$PID" > /dev/null 2>&1; then
    echo "IMA ALREADY RUNNING"
    exit 0
  fi
fi

nohup node ima.js > logs/runtime.log 2>&1 &

PID=$!

echo "$PID" > "$LOCK"

sleep 2

curl -s http://127.0.0.1:7000/health || echo "BOOT FAILED"
