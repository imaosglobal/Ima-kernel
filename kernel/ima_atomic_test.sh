#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA ATOMIC FLOW TEST ==="

# 1. create user
SIGNUP=$(curl -s -X POST http://localhost:4000/v1/signup)

echo "[1] signup response:"
echo "$SIGNUP"

# extract key safely
KEY=$(echo "$SIGNUP" | grep -o '"apiKey":"[^"]*"' | cut -d'"' -f4)

echo "[2] extracted key: $KEY"

if [ -z "$KEY" ]; then
  echo "[ERROR] No API key generated"
  exit 1
fi

# 2. run test using same key
RUN=$(curl -s -X POST http://localhost:4000/v1/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"atomic test hello"}')

echo "[3] run result:"
echo "$RUN"

echo "=== DONE ==="
