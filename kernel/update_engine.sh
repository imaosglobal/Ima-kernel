#!/data/data/com.termux/files/usr/bin/bash

ROOT=/data/data/com.termux/files/home/ima_core/kernel
LOG=$ROOT/server.log

echo "[UPDATE] starting sync" | tee -a $LOG

cd $ROOT

# 1. fetch remote
git fetch origin main >> $LOG 2>&1

# 2. pull remote changes
git pull origin main >> $LOG 2>&1

# 3. check local changes
if [ -n "$(git status --porcelain)" ]; then
  echo "[UPDATE] local changes detected - committing" | tee -a $LOG

  git add .
  git commit -m "auto sync $(date)" >> $LOG 2>&1

  git push origin main >> $LOG 2>&1
fi

# 4. install deps
npm install >> $LOG 2>&1

# 5. restart system
bash $ROOT/executor.sh restart >> $LOG 2>&1

echo "[UPDATE] done" | tee -a $LOG
