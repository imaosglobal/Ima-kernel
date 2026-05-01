#!/data/data/com.termux/files/usr/bin/bash

ROOT=/data/data/com.termux/files/home/ima_core/kernel
LOG=$ROOT/server.log

echo "[UPDATE] START" | tee -a $LOG

cd $ROOT

# 1. FETCH + PULL
echo "[UPDATE] pulling..." | tee -a $LOG
git fetch origin main >> $LOG 2>&1
git pull origin main >> $LOG 2>&1

# 2. LOCAL CHANGES
if [ -n "$(git status --porcelain)" ]; then
  echo "[UPDATE] committing local changes..." | tee -a $LOG

  git add .
  git commit -m "auto sync $(date)" >> $LOG 2>&1
  git push origin main >> $LOG 2>&1
fi

# 3. INSTALL
echo "[UPDATE] installing deps..." | tee -a $LOG
npm install >> $LOG 2>&1

# 4. SINGLE RESTART (FIXED DUPLICATION BUG)
echo "[UPDATE] restarting system..." | tee -a $LOG
bash $ROOT/executor.sh restart >> $LOG 2>&1

echo "[UPDATE] DONE" | tee -a $LOG
