#!/data/data/com.termux/files/usr/bin/bash

BASE="/data/data/com.termux/files/home/ima_core/ima_bundle/unified_ima/ima_unified_system"
LOG="$BASE/cron_brain.log"

echo "===== CRON BRAIN START $(date) =====" >> $LOG

# 1. HEALTH CHECK
echo "[1] health check..." >> $LOG
node $BASE/ima_boot.js 2>&1 | tee -a $LOG || echo "health check failed" >> $LOG

# 2. SERVER CHECK
echo "[2] server check..." >> $LOG
curl -s http://localhost:3000/state >> $LOG || echo "server offline" >> $LOG

# 3. GIT SYNC
echo "[3] git sync..." >> $LOG
bash $BASE/git_auto_sync.sh >> $LOG 2>&1

# 4. CLEANUP SAFE
echo "[4] cleanup..." >> $LOG
rm -f $BASE/tmp_* 2>/dev/null

# 5. SNAPSHOT SAFE
echo "[5] snapshot..." >> $LOG
node $BASE/ima_kernel.js snapshot >> $LOG 2>&1 || echo "snapshot failed" >> $LOG

echo "===== CRON BRAIN END $(date) =====" >> $LOG
