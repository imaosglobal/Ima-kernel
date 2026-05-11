#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA DAILY SYSTEM CHECK ==="

BASE="http://localhost:4000"

# 1. check server
HEALTH=$(curl -s $BASE/run \
  -H "x-api-key: test" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"health"}')

echo "[1] health check:"
echo "$HEALTH"

# 2. detect failure
if echo "$HEALTH" | grep -q "error"; then
  echo "[!] system degraded → running auto_pipeline"
  bash ~/ima_core/kernel/auto_pipeline.sh
else
  echo "[✓] system OK"
fi

# 3. log snapshot
echo "$(date) - $HEALTH" >> ~/ima_core/kernel/daily.log

echo "=== DONE ==="
