#!/data/data/com.termux/files/usr/bin/bash

FILE="$HOME/ima_core/server.js"
TMP="$HOME/ima_core/_tmp_server.js"
BACKUP="$HOME/ima_core/server_backup.js"

echo "🧠 SAFE EDIT v3"

# תמיד עובדים על עותק
cp "$FILE" "$TMP"

# מריצים את הפקודה על העותק בלבד
"$@" "$TMP"

# בדיקת תחביר על העותק
node -c "$TMP"
if [ $? -ne 0 ]; then
  echo "❌ Invalid change - discarding"
  rm "$TMP"
  exit 1
fi

# אם תקין → החלפה
cp "$FILE" "$BACKUP"
cp "$TMP" "$FILE"

echo "✔ SAFE CHANGE APPLIED"
