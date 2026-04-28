#!/data/data/com.termux/files/usr/bin/bash

BASE="/data/data/com.termux/files/home/ima_core/ima_bundle/unified_ima/ima_unified_system"
LOG="$BASE/cron_brain.log"

echo "===== CRON BRAIN START $(date) =====" >> $LOG

cd $BASE || exit 1

# =========================
# 1. HEALTH CHECK
# =========================
echo "[1] health check..." >> $LOG
node ima_boot.js --check >> $LOG 2>&1

if [ $? -ne 0 ]; then
  echo "⚠ kernel unhealthy -> restart attempt" >> $LOG
  node ima_boot.js >> $LOG 2>&1 &
fi

# =========================
# 2. SERVER CHECK
# =========================
echo "[2] server check..." >> $LOG
curl -s http://localhost:3000/state > /dev/null

if [ $? -ne 0 ]; then
  echo "⚠ server down -> restarting" >> $LOG
  node server.js >> $LOG 2>&1 &
fi

# =========================
# 3. GIT SYNC (safe push only)
# =========================
echo "[3] git sync..." >> $LOG

./git_auto_sync.sh >> $LOG 2>&1

# =========================
# 4. CLEANUP
# =========================
echo "[4] cleanup..." >> $LOG

find . -name "*.log" -mtime +7 -delete >> $LOG 2>&1

# =========================
# 5. SNAPSHOT STATE
# =========================
echo "[5] snapshot..." >> $LOG

node ima_kernel.js snapshot > $BASE/state_snapshot.json 2>/dev/null

echo "===== CRON BRAIN END =====" >> $LOG
echo "" >> $LOG
