#!/data/data/com.termux/files/usr/bin/bash

BASE="http://localhost:4000"
KEY=$(cat ~/.ima_key 2>/dev/null)

if [ -z "$KEY" ]; then
  echo "No API key found. Creating one..."
  RESP=$(curl -s -X POST $BASE/signup)
  KEY=$(echo $RESP | sed -E 's/.*"apiKey":"([^"]+)".*/\1/')
  echo $KEY > ~/.ima_key
  echo "Saved API key."
fi

TASK="$1"

curl -s -X POST $BASE/run \
  -H "x-api-key: $KEY" \
  -H "Content-Type: application/json" \
  --data-raw "{\"task\":\"$TASK\"}"
echo ""
