#!/data/data/com.termux/files/usr/bin/bash
echo "=== הגדרת אמא בפעם הראשונה 💛 ==="
echo ""

if [ -z "$GEMINI_API_KEY" ]; then
  read -p "הדבק את מפתח GEMINI_API_KEY: " key
  echo "export GEMINI_API_KEY=\"$key\"" >> ~/.bashrc
  export GEMINI_API_KEY="$key"
  echo "נשמר!"
fi

if [ -z "$SUPABASE_URL" ]; then
  read -p "הדבק את SUPABASE_URL: " url
  echo "export SUPABASE_URL=\"$url\"" >> ~/.bashrc
  export SUPABASE_URL="$url"
fi

if [ -z "$SUPABASE_KEY" ]; then
  read -p "הדבק את SUPABASE_KEY: " skey
  echo "export SUPABASE_KEY=\"$skey\"" >> ~/.bashrc
  export SUPABASE_KEY="$skey"
fi

echo ""
echo "=== מותקן! מרים את אמא ברקע ==="
pkill -9 python 2>/dev/null
nohup python -m uvicorn main:app --host 127.0.0.1 --port 8000 > server.log 2>&1 &
sleep 3
curl -s http://127.0.0.1:8000/docs > /dev/null && echo "אמא עלתה ורצה 💛" || echo "יש בעיה - תריץ: cat server.log"
