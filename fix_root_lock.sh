#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_kernel"

echo "[1] enforcing root: $ROOT"

# ליצור משתנה סביבה קבוע
if ! grep -q "IMA_ROOT" ~/.bashrc; then
  echo "export IMA_ROOT=$ROOT" >> ~/.bashrc
fi

# לתקן server.js כך שלא ישתמש ב-~ או paths חיצוניים
SERVER="$ROOT/server.js"

sed -i "s|process.env.HOME|process.env.IMA_ROOT || process.env.HOME|g" "$SERVER" || true

# לוודא runtime/logs בתוך kernel בלבד
mkdir -p "$ROOT/runtime/logs"

# הוספת רישום לזיכרון אם קיים memory
MEM="$ROOT/kernel/core/memory.js"

if [ -f "$MEM" ]; then
  echo "[2] memory already exists - appending trace"
fi

# יצירת תיעוד מצב
mkdir -p "$ROOT/kernel/memory"
echo "{\"event\":\"root_locked\",\"time\":$(date +%s)}" >> "$ROOT/kernel/memory/bootstrap_trace.json"

# restart נקי
echo "[3] restarting kernel"
pkill -f server.js || true
sleep 1
nohup node "$SERVER" > "$ROOT/runtime/logs/server.log" 2>&1 &

echo "[DONE] ima_kernel locked to single root"
