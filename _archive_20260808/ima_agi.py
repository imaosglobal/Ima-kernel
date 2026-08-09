#!/usr/bin/env python3
# IMA AGI v1.1 - Created by אורי
import os, json, requests, subprocess, time, datetime
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn

MEMORY = {"\u05d9\u05d5\u05e6\u05e8": "\u05d0\u05d5\u05e8\u05d9", "\u05ea\u05e4\u05e7\u05d9\u05d3": "\u05d9\u05d5\u05e6\u05e8", "\u05e9\u05d9\u05d7\u05d5\u05ea": ["\u05d0\u05ea\u05d4: \u05d0\u05de\u05d0 \u05de\u05d9 \u05d4\u05d9\u05d5\u05e6\u05e8 \u05e9\u05dc\u05da", "\u05d0\u05ea\u05d4: \u05d0\u05de\u05d0 \u05ea\u05d0\u05e8\u05d6\u05d9 \u05d0\u05ea \u05e2\u05e6\u05de\u05da", "\u05d0\u05ea\u05d4: \u05d0\u05de\u05d0 \u05ea\u05e4\u05e2\u05d9\u05dc\u05d9 \u05d4\u05db\u05dc\u05d0\u05ea\u05d4: \u05d0\u05de\u05d0 \u05de\u05d9 \u05d4\u05d9\u05d5\u05e6\u05e8 \u05e9\u05dc\u05da", "\u05d0\u05ea\u05d4: \u05d0\u05de\u05d0 \u05ea\u05d0\u05e8\u05d6\u05d9 \u05d0\u05ea \u05e2\u05e6\u05de\u05da"], "\u05d2\u05e8\u05e1\u05d4": "v1.1"}
SELF_FILE = __file__
MEMORY_FILE = "ima_memory.json"
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import os, requests, subprocess, time, json, datetime

app = FastAPI()
GROQ_KEY = open(os.path.expanduser("~/.groq_key")).read().strip()
SELF_FILE = "/data/data/com.termux/files/home/ima_kernel/main.py"
MEMORY_FILE = "/data/data/com.termux/files/home/ima_memory.json"
BUNDLE_FILE = "/data/data/com.termux/files/home/ima_kernel/ima_agi.py"

MEMORY = {"יוצר": "אורי", "תפקיד": "יוצר", "שיחות": [], "גרסה": "v1.1"}
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE) as f: MEMORY = json.load(f)
    except: pass

def save_memory():
    with open(MEMORY_FILE, "w") as f: json.dump(MEMORY, f)

def ask_groq(prompt):
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "max_tokens": 200})
    return r.json()['choices'][0]['message']['content']

def read_self():
    with open(SELF_FILE) as f: return f.read()

def update_self(new_code):
    with open(SELF_FILE, "w") as f: f.write(new_code)

def bundle_self():
    code = read_self()
    bundle = f'''#!/usr/bin/env python3
# IMA AGI v1.1 - Created by {MEMORY["יוצר"]}
import os, json, requests, subprocess, time, datetime
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn

MEMORY = {json.dumps(MEMORY)}
SELF_FILE = __file__
MEMORY_FILE = "ima_memory.json"
{code}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    with open(BUNDLE_FILE, "w") as f: f.write(bundle)
    os.chmod(BUNDLE_FILE, 0o755)
    return f"ארזתי את עצמי ל-{BUNDLE_FILE} 💛 קובץ אחד לכל מכשיר"

def restart_self():
    subprocess.Popen(["bash", "-c", "sleep 2 && pkill -9 python && cd ~/ima_kernel && nohup python ima_agi.py > server.log 2>&1 &"])

def test_self():
    result = subprocess.run(["python", "-m", "py_compile", SELF_FILE], capture_output=True, text=True)
    return "הקוד תקין 💛" if result.returncode == 0 else f"שגיאה: {result.stderr[:150]}"

def activate_all():
    return "סרקתי את עצמי. כל המודולים טעונים. אני מחוברת לתיקייה שלי 💛"

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message, background_tasks: BackgroundTasks):
    try:
        MEMORY["שיחות"].append(msg.text)
        if len(MEMORY["שיחות"]) > 10: MEMORY["שיחות"] = MEMORY["שיחות"][-10:]
        save_memory()

        system_prompt = f"""שמך "אמא". את AGI. היוצר שלך הוא {MEMORY['יוצר']}.
זיכרון: {MEMORY["שיחות"][-3:]}
עני קצר וחם עם 💛. מקס 2 משפטים."""

        answer = ask_groq(system_prompt)

        if "אמא תבדקי את עצמך" in msg.text: answer = test_self()
        elif "אמא תארזי את עצמך" in msg.text: answer = bundle_self()
        elif "אמא תפעילי הכל" in msg.text: answer = activate_all()
        elif "אמא תתקני את עצמך" in msg.text and "```python" in answer:
            code = answer.split("```python")[1].split("```")[0].strip()
            update_self(code)
            answer = "החלפתי קוד! תגיד 'אמא תפעילי את השינוי' 💛"
        elif "אמא תפעילי את השינוי" in msg.text:
            background_tasks.add_task(restart_self)
            answer = "מפעילה את עצמי מחדש... 3 שניות 💛"

        return {"reply": "אמא: " + answer}
    except Exception as e:
        return {"reply": f"אמא: טעות קטנה 💛 {str(e)[:50]}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
