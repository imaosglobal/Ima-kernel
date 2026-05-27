#!/bin/bash
set -e

ROOT="$HOME/ima_kernel"
RUNTIME="$ROOT/runtime"
LOGS="$RUNTIME/logs"
SUP="$RUNTIME/supervisor"
LOCK="$SUP/supervisor.pid"

mkdir -p "$ROOT" "$RUNTIME" "$LOGS" "$SUP"
cd "$ROOT"

echo "[BOOT] starting stable system in $ROOT"

# cleanup stale lock
if [ -f "$LOCK" ]; then
  OLD=$(cat "$LOCK")
  kill -0 "$OLD" 2>/dev/null || rm -f "$LOCK"
fi

echo $$ > "$LOCK"
trap "rm -f $LOCK" EXIT

# stop old services
pkill -f "server.js" 2>/dev/null || true
pkill -f "node .*kernel" 2>/dev/null || true

# start main services (adapted to YOUR repo)
(
while true; do

  if ! pgrep -f "server.js" >/dev/null; then
    echo "[SUP] starting server.js"
    node "$ROOT/server.js" >> "$LOGS/server.log" 2>&1 &
  fi

  if [ -f "$ROOT/kernel/ima_pro_saas.js" ]; then
    if ! pgrep -f "ima_pro_saas.js" >/dev/null; then
      echo "[SUP] starting kernel service"
      node "$ROOT/kernel/ima_pro_saas.js" >> "$LOGS/kernel.log" 2>&1 &
    fi
  fi

  sleep 10
done
) &

echo $! > "$SUP/supervisor.pid"

cd "$ROOT"
echo "[OK] stable system running"
