#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

cd "$ROOT"

pkill -f "node" 2>/dev/null || true

sleep 1

nohup node ima.js > "$ROOT/logs/runtime.log" 2>&1 &

sleep 2

curl -s http://127.0.0.1:7000/health || echo "BOOT FAILED"
