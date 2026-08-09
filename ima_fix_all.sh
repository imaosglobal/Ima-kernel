#!/bin/bash
echo "[1/5] מוחק קבצי סוד מההיסטוריה..."
git filter-repo --path .env --path .env.production --path .env.production.broken_backup --invert-paths --force

echo "[2/5] יוצר קובץ env ריק ובטוח..."
echo "# IMA ENV - DO NOT COMMIT SECRETS" > .env
echo "SUPABASE_URL=your_url_here" >> .env
echo "SUPABASE_KEY=your_key_here" >> .env

echo "[3/5] מוסיף ל-gitignore..."
echo ".env" >> .gitignore
echo ".env.production" >> .gitignore
git add .gitignore .env
git commit -m "Remove secrets and add gitignore"

echo "[4/5] מחזיר remote אם נמחק..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/imaosglobal/Ima-kernel.git

echo "[5/5] דוחף לגיטהאב..."
git push -u origin main --force

echo "=== DONE ==="
echo "עכשיו כנס לSupabase ותחליף את הAPI KEY כי הישן דלף"
