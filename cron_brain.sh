#!/data/data/com.termux/files/usr/bin/bash

BASE="/data/data/com.termux/files/home/ima_core/ima_bundle/unified_ima/ima_unified_system"
LOG="$BASE/cron_brain.log"

echo "===== CRON BRAIN START $(date) =====" >> $LOG

# 1. HEALTH CHECK (ללא boot מלא!)
echo "[1] health check..." >> $LOG
node $BASE/ima_boot.js --status 2>/dev/null >> $LOG || echo "health failed" >> $LOG

# 2. SERVER CHECK + SAFE RESTART
echo "[2] server check..." >> $LOG
if curl -s --max-time 2 http://localhost:3000/state >/dev/null; then
  echo "server ok" >> $LOG
else
  echo "server offline -> restart" >> $LOG
  pkill -f "node.*server.js" || true
  nohup node $BASE/server.js >/dev/null 2>&1 &
fi

# 3. GIT SYNC
echo "[3] git sync..." >> $LOG
bash $BASE/git_auto_sync.sh >> $LOG 2>&1

# 4. CLEAN SAFE
echo "[4] cleanup..." >> $LOG
rm -f $BASE/tmp_* 2>/dev/null

# 5. SNAPSHOT LOCKED (מונע לולאה)
echo "[5] snapshot..." >> $LOG
if [ ! -f "$BASE/.snapshot_lock" ]; then
  touch "$BASE/.snapshot_lock"
  node $BASE/ima_kernel.js snapshot >> $LOG 2>&1 || echo "snapshot failed" >> $LOG
  rm -f "$BASE/.snapshot_lock"
else
  echo "snapshot skipped (locked)" >> $LOG
fi

echo "===== CRON BRAIN END $(date) =====" >> $LOG
