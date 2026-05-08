#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

# === HEALTH CHECK ===
if ! curl -s http://localhost:4000/run \
  -H "x-api-key: $(cat ~/.ima_key)" \
  -H "Content-Type: application/json" \
  --data-raw '{"task":"health"}' | grep -q ok; then

  echo "SERVER DOWN → restarting"
  pkill -f ima_pro_saas.js || true
  node ~/ima_core/kernel/ima_pro_saas.js &
fi

# === BACKUP DB ===
mkdir -p ~/ima_core/kernel/backups
cp ima_db.json backups/db_$(date +%F).json 2>/dev/null

# === PROCESS GUARD ===
pgrep -f ima_pro_saas.js >/dev/null || node ~/ima_core/kernel/ima_pro_saas.js &
