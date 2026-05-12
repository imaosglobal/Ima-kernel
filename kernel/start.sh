#!/data/data/com.termux/files/usr/bin/bash

pkill -f "runtime/server.js" 2>/dev/null || true
pkill -f "runtime/autonomous_runtime.js" 2>/dev/null || true

sleep 2

nohup node runtime/autonomous_runtime.js > logs/runtime.log 2>&1 &
