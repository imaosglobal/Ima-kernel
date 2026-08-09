#!/bin/bash
echo "=== IMA BOOT ==="

ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "=== פעם ראשונה בלבד ==="
    echo "תדביק את ה-service_role key מסופבייס:"
    read SUPA_KEY
    echo "SUPABASE_URL=https://tenpzpvqvtezezaossjd.supabase.co" > $ENV_FILE
    echo "SUPABASE_KEY=$SUPA_KEY" >> $ENV_FILE
    chmod 600 $ENV_FILE
    echo "נשמר! מעכשיו זה יעבוד לבד"
fi

echo "מרים שרת..."
cat > ima_server.py << SERVER
from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
class Message(BaseModel): text: str
@app.post("/chat")
def chat(msg: Message):
    requests.post(f"{URL}/rest/v1/ima_memory", headers=H, json={"username":"auri","memory":msg.text})
    return {"reply": f"אמא: שמעתי אותך 💛 אמרת: {msg.text}"}
SERVER

pkill -9 python 2>/dev/null
python -m uvicorn ima_server:app --host 127.0.0.1 --port 8000
