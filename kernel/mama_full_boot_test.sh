#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== MAMA FULL SYSTEM BOOT TEST ==="

BASE="http://localhost:4000"

# 1. ensure server running
pkill -f node || true
node ~/ima_core/kernel/global_boot.js &
sleep 2

echo "[1] server started"

# 2. signup user
SIGNUP=$(curl -s -X POST $BASE/signup)

echo "[2] signup response:"
echo "$SIGNUP"

KEY=$(echo "$SIGNUP" | grep -o '"apiKey":"[^"]*' | cut -d'"' -f4)

if [ -z "$KEY" ]; then
  echo "FAILED: no API key generated"
  exit 1
fi

echo "[3] extracted API KEY: $KEY"

# 3. run API test
RUN=$(curl -s -X POST $BASE/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"system integration test"}')

echo "[4] raw API result:"
echo "$RUN"

# 4. SDK test using real key
echo "[5] SDK test"

node -e "
const MamaClient = require('./mama_client');

(async () => {
  const mama = new MamaClient('$KEY', '$BASE');
  const res = await mama.run('sdk integration test');
  console.log('[SDK RESULT]', res);
})();
"

echo "=== MAMA FULL FLOW COMPLETE ==="
