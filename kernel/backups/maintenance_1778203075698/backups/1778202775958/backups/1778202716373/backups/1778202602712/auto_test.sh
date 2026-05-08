#!/data/data/com.termux/files/usr/bin/bash

BASE="http://localhost:4000"

echo "=== AUTO SAAS TEST START ==="

echo "[1] Creating user..."
RESP=$(curl -s -X POST $BASE/signup)
echo "Response: $RESP"

KEY=$(echo $RESP | sed -E 's/.*"apiKey":"([^"]+)".*/\1/')
echo "[2] API KEY: $KEY"

echo "[3] Calling run..."
RUN_RESP=$(curl -s -X POST $BASE/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"hello auto"}')

echo "[4] RESULT:"
echo $RUN_RESP

echo "=== DONE ==="
