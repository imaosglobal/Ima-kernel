#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "=== IMA TEST FLOW ==="

SIGNUP=$(curl -s -X POST http://localhost:4000/v1/signup)

echo "[1] signup:"
echo "$SIGNUP"

KEY=$(echo "$SIGNUP" | grep -o '"apiKey":"[^"]*"' | cut -d'"' -f4)

if [ -z "$KEY" ]; then
  echo "[ERROR] missing api key"
  exit 1
fi

echo "[2] key: $KEY"

RUN=$(curl -s -X POST http://localhost:4000/v1/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"ima test"}')

echo "[3] result:"
echo "$RUN"

echo "=== DONE ==="
