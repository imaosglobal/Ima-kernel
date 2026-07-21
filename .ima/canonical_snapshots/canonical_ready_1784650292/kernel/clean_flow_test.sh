#!/data/data/com.termux/files/usr/bin/bash

BASE="http://localhost:4000"

echo "=== CLEAN IMA FLOW TEST ==="

# 1. signup
SIGNUP=$(curl -s -X POST $BASE/signup)

echo "[1] signup response:"
echo "$SIGNUP"

KEY=$(echo "$SIGNUP" | grep -o '"apiKey":"[^"]*' | cut -d'"' -f4)

echo "[2] extracted key: $KEY"

# 2. run test
RUN=$(curl -s -X POST $BASE/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"clean test"}')

echo "[3] run result:"
echo "$RUN"

echo "=== DONE ==="
