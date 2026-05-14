#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"

cd "$ROOT"

pkill -f "node ima.js" 2>/dev/null || true

nohup node ima.js > "$ROOT/logs/runtime.log" 2>&1 &

echo "IMA STARTED"
