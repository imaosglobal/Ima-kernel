#!/data/data/com.termux/files/usr/bin/bash

BASE_LOCAL="http://localhost:4000"

echo "=== IMA FULL SYSTEM CHECK ==="

# 1. בדיקה אם השרת רץ
echo "[1] Checking server..."
RUNNING=$(ps aux | grep ima_pro_saas.js | grep -v grep)

if [ -z "$RUNNING" ]; then
  echo "Server not running. Starting..."
  node ~/ima_core/kernel/ima_pro_saas.js &
  sleep 2
else
  echo "Server already running"
fi

# 2. בדיקה מקומית
echo "[2] Local test..."
RESP=$(curl -s -X POST $BASE_LOCAL/signup)

if [[ $RESP != *apiKey* ]]; then
  echo "❌ Local signup failed"
  exit 1
fi

KEY=$(echo $RESP | sed -E 's/.*"apiKey":"([^"]+)".*/\1/')
echo "Local KEY: $KEY"

RUN=$(curl -s -X POST $BASE_LOCAL/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"local test"}')

echo "Local run result: $RUN"

if [[ $RUN != *ok* ]]; then
  echo "❌ Local run failed"
  exit 1
fi

echo "✔ Local system OK"

# 3. פתיחת tunnel
echo "[3] Starting tunnel..."
ssh -o StrictHostKeyChecking=no -R 80:localhost:4000 serveo.net > ~/ima_core/kernel/ima_tunnel.txt 2>&1 &
sleep 3

URL=$(grep -o 'https://[a-zA-Z0-9.-]*serveousercontent.com' ~/ima_core/kernel/ima_tunnel.txt | head -n1)

if [ -z "$URL" ]; then
  echo "❌ Tunnel failed"
  cat ~/ima_core/kernel/ima_tunnel.txt
  exit 1
fi

echo "Tunnel URL: $URL"

# 4. בדיקה חיצונית
echo "[4] External signup..."
RESP_EXT=$(curl -s -X POST $URL/signup)

if [[ $RESP_EXT != *apiKey* ]]; then
  echo "❌ External signup failed"
  exit 1
fi

KEY_EXT=$(echo $RESP_EXT | sed -E 's/.*"apiKey":"([^"]+)".*/\1/')
echo "External KEY: $KEY_EXT"

RUN_EXT=$(curl -s -X POST $URL/run \
  -H "x-api-key: $KEY_EXT" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"external test"}')

echo "External run result: $RUN_EXT"

if [[ $RUN_EXT != *ok* ]]; then
  echo "❌ External run failed"
  exit 1
fi

echo "✔ EXTERNAL SYSTEM OK"

echo "=== SYSTEM FULLY WORKING ==="
