#!/data/data/com.termux/files/usr/bin/bash

LOCK=/data/data/com.termux/files/home/ima_kernel/runtime/server.lock

echo "[FIX] enforcing single instance..."

# kill all existing
pkill -f server.js || true
pkill -f watchdog.sh || true

# wait cleanup
sleep 2

# remove stale lock
rm -f "$LOCK"

# start server with lock
(
  if [ -f "$LOCK" ]; then
    echo "[SKIP] server already running"
    exit 0
  fi

  echo $$ > "$LOCK"

  echo "[START] server.js"
  nohup node ~/ima_kernel/server.js > ~/ima_kernel/runtime/logs/server.log 2>&1 &

  echo "[START] watchdog.sh"
  nohup bash ~/ima_kernel/watchdog.sh > ~/ima_kernel/runtime/logs/watchdog.log 2>&1 &
)

echo "[DONE] single instance enforced"
