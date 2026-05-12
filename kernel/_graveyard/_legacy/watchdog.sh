#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

LOCKFILE=~/ima_core/kernel/watchdog.lock

# prevent duplicates
if [ -f "$LOCKFILE" ]; then
  PID=$(cat "$LOCKFILE")
  if ps -p $PID > /dev/null 2>&1; then
    echo "[WATCHDOG] already running (PID $PID)"
    exit 0
  fi
fi

echo $$ > "$LOCKFILE"

FAIL=0

while true; do

  HEALTH=$(curl -s http://localhost:4000/health || echo "down")

  if echo "$HEALTH" | grep -q "alive"; then
    FAIL=0
  else
    FAIL=$((FAIL+1))
  fi

  if [ "$FAIL" -ge 3 ]; then
    echo "[WATCHDOG] restart triggered"

    pkill -f prod_server.js || true
    sleep 2
    nohup node prod_server.js > server.log 2>&1 &

    FAIL=0
  fi

  cat > ima_state.json << EOC
{
  "version": "1.0.0",
  "status": "running",
  "last_check": "$(date)",
  "health": $HEALTH,
  "fail_count": $FAIL
}
EOC

  sleep 20
done
