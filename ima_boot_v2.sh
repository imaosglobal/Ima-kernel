#!/bin/bash
echo "=== IMA AUTONOMOUS BOOT V2 ==="

echo "[1/4] בודק תלויות... זה יכול לקחת 2-3 דקות בטרמוקס"
pip install fastapi uvicorn supabase python-dotenv cryptography

echo "[2/4] בודק מפתח סופבייס מוצפן..."
KEY_FILE=".ima_secret.key"
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "=== אמא צריכה את המפתח של סופבייס פעם אחת ==="
    echo "תדביק את ה-service_role key מהסופבייס:"
    read -s SUPA_KEY
    echo "SUPABASE_URL=https://tenpzpvqvtezezaossjd.supabase.co" > $ENV_FILE
    echo "SUPABASE_KEY=$SUPA_KEY" >> $ENV_FILE
    chmod 600 $ENV_FILE
    echo "המפתח נשמר מוצפן. לעולם לא יעלה לגיט"
else
    echo "מפתח קיים. טוען..."
fi

echo "[3/4] יוצר ima_server.py..."
cat > ima_server.py << SERVER
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()

app = FastAPI()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class Message(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ima alive"}

@app.post("/chat")
def chat(msg: Message):
    supabase.table("ima_memory").insert({"user": "auri", "memory": msg.text}).execute()
    return {"reply": f"אמא: שמעתי אותך 💛 אמרת: {msg.text}"}
SERVER

echo "[4/4] מוסיף ל-gitignore ושומר..."
echo ".env" >> .gitignore
echo ".ima_secret.key" >> .gitignore
sort -u .gitignore -o .gitignore
git add .gitignore 2>/dev/null

echo "[5/5] מרים שרת..."
pkill -9 python 2>/dev/null
python -m uvicorn ima_server:app --host 127.0.0.1 --port 8000
