#!/data/data/com.termux/files/usr/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

while true; do
  echo "🧠 IMA CORE LOOP..."
  cd "$BASE_DIR"
  node ima_core_engine.js "daily evolution"

  sleep 86400
done
