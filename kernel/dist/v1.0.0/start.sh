#!/bin/bash

pkill -f "runtime/ENTRYPOINT.js" 2>/dev/null || true
sleep 1

nohup node runtime/ENTRYPOINT.js > logs/runtime.log 2>&1 &

sleep 1
pgrep -af ENTRYPOINT
