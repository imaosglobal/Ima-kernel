#!/data/data/com.termux/files/usr/bin/bash

FILE="$HOME/ima_core/server.js"
TMP="$HOME/ima_core/tmp.js"
BACKUP="$HOME/ima_core/server_backup.js"

echo "🧠 SAFE APPLY MODE"

# יצירת snapshot לפני שינוי
cp "$FILE" "$TMP"

# הרצת הפקודה על tmp בלבד
"$@"

# בדיקת syntax על tmp
node -c "$TMP"
if [ $? -ne 0 ]; then
  echo "❌ Invalid change → discarding"
  rm "$TMP"
  exit 1
fi

# אם תקין → החלפה
cp "$FILE" "$BACKUP"
cp "$TMP" "$FILE"

echo "✔ Change applied safely"
