#!/bin/bash

set -e

echo "=== CI START ==="

echo "[1] start temp runtime"
pkill -f ENTRYPOINT || true

nohup node runtime/ENTRYPOINT.js > logs/ci.log 2>&1 &
sleep 3

echo "[2] health check"

STATE=$(node -e "console.log(require('./runtime/KERNEL_STATE').getState())")

echo "$STATE" | grep -q "alive" || {
  echo "CI FAILED: runtime not healthy"
  exit 1
}

echo "[3] heartbeat check"

node -e "
const k=require('./runtime/KERNEL_STATE');
setTimeout(()=>{
  const s=k.getState();
  if(!s.lastHeartbeat) process.exit(1);
  console.log('HEARTBEAT OK');
},2000);
"

sleep 3

echo "=== CI PASSED ==="
