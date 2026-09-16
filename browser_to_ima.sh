#!/data/data/com.termux/files/usr/bin/bash

set -e

TEXT="$(termux-clipboard-get 2>/dev/null || true)"

if [ -z "$TEXT" ]; then
    echo "ERROR: CLIPBOARD_EMPTY"
    exit 1
fi

RESULT="$(curl -s -X POST \
  -H 'Content-Type: text/plain; charset=utf-8' \
  --data-binary "$TEXT" \
  http://127.0.0.1:8765/ingest)"

echo "$RESULT"

if [ "$RESULT" = "INGESTED" ]; then
    echo "IMA_BROWSER_BRIDGE: INGESTED"
elif [ "$RESULT" = "DUPLICATE" ]; then
    echo "IMA_BROWSER_BRIDGE: DUPLICATE"
else
    echo "IMA_BROWSER_BRIDGE: ERROR"
    exit 1
fi
