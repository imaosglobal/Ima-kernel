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
