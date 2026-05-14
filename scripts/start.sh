#!/bin/bash

ROOT="$HOME/ima_kernel"

pkill -f "node kernel/index.js" || true

nohup node "$ROOT/kernel/index.js" > "$ROOT/logs/core.log" 2>&1 &

sleep 2
curl -s localhost:3000/health
