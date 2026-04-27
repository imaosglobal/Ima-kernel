#!/data/data/com.termux/files/usr/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

while true; do
  echo "🧠 Running daily cycle..."
  cd "$BASE_DIR"
  ./ima_full_cycle.sh

  sleep 86400
done
