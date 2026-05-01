#!/data/data/com.termux/files/usr/bin/bash

ROOT=/data/data/com.termux/files/home/ima_core/kernel
LOG=$ROOT/server.log

echo "[UPDATE] START"

cd $ROOT

echo "[UPDATE] pulling..."
PULL_RESULT=$(git pull origin main 2>&1)
echo "$PULL_RESULT"
echo "$PULL_RESULT" >> $LOG

echo "[UPDATE] checking local changes..."
STATUS=$(git status --porcelain)

if [ -n "$STATUS" ]; then
  echo "[UPDATE] committing local changes..."

  git add .
  COMMIT_RESULT=$(git commit -m "auto sync $(date)" 2>&1)
  echo "$COMMIT_RESULT"
  echo "$COMMIT_RESULT" >> $LOG

  PUSH_RESULT=$(git push origin main 2>&1)
  echo "$PUSH_RESULT"
  echo "$PUSH_RESULT" >> $LOG
fi

echo "[UPDATE] installing deps..."
NPM_RESULT=$(npm install 2>&1)
echo "$NPM_RESULT" | tail -n 5
echo "$NPM_RESULT" >> $LOG

echo "[UPDATE] restarting system..."
bash $ROOT/executor.sh restart

echo "[UPDATE] DONE"
