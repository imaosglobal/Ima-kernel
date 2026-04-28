#!/data/data/com.termux/files/usr/bin/bash

cd "$(dirname "$0")"

echo "🔄 Git auto sync starting..."

# בדיקה שיש שינויים
if [[ -n $(git status --porcelain) ]]; then
  echo "📦 Changes detected - committing..."

  git add -A
  git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"

  git push origin main

  echo "✅ Synced to remote"
else
  echo "✔ No changes to sync"
fi
