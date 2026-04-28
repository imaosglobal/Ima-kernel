#!/data/data/com.termux/files/usr/bin/bash

BASE="/data/data/com.termux/files/home/ima_core/ima_bundle/unified_ima/ima_unified_system"
LOCK="$BASE/ima_sync.lock"

# אם נעול → יציאה שקטה
if [ -f "$LOCK" ]; then
  echo "SYNC BLOCKED (LOCKED)" >> "$BASE/cron_brain.log"
  exit 0
fi

bash "$BASE/git_auto_sync.sh"
