#!/data/data/com.termux/files/usr/bin/bash

while true; do
  echo "🧠 Running daily cycle..."
  cd ~/ima_unified_system/ima_product
  ./ima_full_cycle.sh

  # 24 שעות
  sleep 86400
done
