#!/data/data/com.termux/files/usr/bin/bash

FILE="$HOME/ima_core/server.js"
BACKUP="$HOME/ima_core/server_backup.js"

echo "🧠 Starting SAFE IMA runtime..."

# בדיקת תחביר לפני הרצה
node -c "$FILE"
if [ $? -ne 0 ]; then
  echo "❌ SYNTAX ERROR DETECTED - rolling back"
  cp "$BACKUP" "$FILE"
  node -c "$FILE"
  if [ $? -ne 0 ]; then
    echo "💥 Backup also broken. Manual fix required."
    exit 1
  fi
fi

# יצירת backup לפני ריצה
cp "$FILE" "$BACKUP"

# הרצה
node "$FILE"
