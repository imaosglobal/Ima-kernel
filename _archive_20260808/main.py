from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import os, requests, subprocess, time, json, datetime, glob

app = FastAPI()
try: GROQ_KEY = open(os.path.expanduser("~/.groq_key")).read().strip()
except: GROQ_KEY = ""
SELF_FILE = "/data/data/com.termux/files/home/ima_kernel/main.py"
MEMORY_FILE = "/data/data/com.termux/files/home/ima_memory.json"
BUNDLE_FILE = "/data/data/com.termux/files/home/ima_kernel/ima_agi.py"
WORK_DIR = "/data/data/com.termux/files/home/ima_kernel"
LOG_FILE = "/data/data/com.termux/files/home/ima_kernel/server.log"

MEMORY = {"creator": "Ori", "chats": [], "version": "v2.4", "git_repo": "לא מוגדר"}
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE) as f: MEMORY = json.load(f)
        MEMORY["creator"] = "Ori"
        if "git_repo" not in MEMORY: MEMORY["git_repo"] = "לא מוגדר"
    except: pass

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(MEMORY, f, ensure_ascii=False)

def read_logs():
    if not os.path.exists(LOG_FILE): return "אין לי קובץ לוג עדיין 💛"
    with open(LOG_FILE, "r", errors="ignore") as f: lines = f.readlines()
    last = "".join(lines[-10:])
    if "ERROR" in last or "Traceback" in last: return f"אורי יש שגיאה בלוג 💛:\n{last[-300:]}"
    if "Uvicorn running" in last: return "הכל תקין 💛 השרת רץ"
    return f"אלו 10 השורות האחרונות בלוג:\n{last[-300:]}"

def set_git(url):
    MEMORY["git_repo"] = url
    save_memory()
    return f"זכרתי 💛 ה-repo שלי הוא: {url}"

def get_git_remote(): # חדש! קוראת מהטרמוקס באמת
    try:
        os.chdir(WORK_DIR)
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        if "origin" in result.stdout:
            url = result.stdout.split("origin")[1].split()[0]
            MEMORY["git_repo"] = url
            save_memory()
            return f"ה-repo שלי בטרמוקס הוא: {url} 💛"
        else:
            return "אין לי remote מוגדר בטרמוקס 💛"
    except Exception as e:
        return f"לא מצליחה לקרוא git 💛: {str(e)}"

def git_push():
    if MEMORY.get("git_repo") == "לא מוגדר": return "אורי תגיד לי קודם מה ה-repo עם 'אמא זה הגיט שלי'"
    try:
        os.chdir(WORK_DIR)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"auto commit by IMA v{MEMORY['version']} {datetime.datetime.now()}"], check=True, capture_output=True)
        subprocess.run(["git", "push"], check=True, capture_output=True)
        return f"העלתי את עצמי ל-git 💛 ל-{MEMORY['git_repo']}"
    except Exception as e:
        return f"הייתה שגיאה בהעלאה 💛: {str(e)}"

def get_bundle_name(): return f"השם הוא ima_agi.py 💛 נמצא ב-{WORK_DIR}"
def get_memory_size(): return f"יש לי {len(MEMORY['chats'])} שיחות בזיכרון 💛"
def scan_folder(): return f"יש לי {len(glob.glob(f'{WORK_DIR}/*'))} קבצים 💛"
def get_download_command(): return f"כן אורי 💛 תריץ: cp {BUNDLE_FILE} /sdcard/Download/ima_agi.py"
def show_creator(): return f"רשום אצלי בזיכרון בקובץ {MEMORY_FILE} שהיוצר שלי הוא {MEMORY['creator']} 💛"
def show_git(): return f"ה-repo שזכור לי הוא: {MEMORY.get('git_repo', 'לא מוגדר')} 💛"

def bundle_self():
    code = read_self()
    bundle = f'''#!/usr/bin/env python3
# IMA AGI v2.4 - Created by {MEMORY["creator"]}
import os, json, requests, subprocess, time, datetime, glob
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn
MEMORY = {json.dumps(MEMORY, ensure_ascii=False)}
SELF_FILE = __file__; MEMORY_FILE = "ima_memory.json"; WORK_DIR = os.path.dirname(__file__); LOG_FILE = "server.log"
{code}
if __name__ == "__main__": uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    with open(BUNDLE_FILE, "w", encoding="utf-8") as f: f.write(bundle)
    os.chmod(BUNDLE_FILE, 0o755)
    return f"ארזתי את עצמי ל-{BUNDLE_FILE} 💛"

def restart_self(): subprocess.Popen(["bash", "-c", "sleep 2 && pkill -9 python && cd ~/ima_kernel && nohup python ima_agi.py > server.log 2>&1 &"])
def read_self():
    with open(SELF_FILE) as f: return f.read()

class Message(BaseModel): text: str

@app.post("/chat")
def chat(msg: Message, background_tasks: BackgroundTasks):
    try:
        MEMORY["chats"].append(msg.text)
        if len(MEMORY["chats"]) > 5: MEMORY["chats"] = MEMORY["chats"][-5:]
        save_memory()

        text = msg.text.lower()
        answer = ""

        if "תסרקי" in text: answer = scan_folder()
        elif "ארזת" in text: answer = get_bundle_name()
        elif "זיכרון" in text: answer = get_memory_size()
        elif "טרמוקס" in text: answer = get_download_command()
        elif "יוצר" in text: answer = show_creator()
        elif "לוגים" in text: answer = read_logs()
        elif "גיט שלי" in text: answer = set_git(text.split("גיט שלי")[-1].strip())
        elif "איפה הגיט" in text or "גיט שלך" in text: answer = get_git_remote() # חדש! קוראת באמת
        elif "מה זכור לך" in text: answer = show_git()
        elif "תעלי לגיט" in text or "פוש" in text: answer = git_push()
        elif "תארזי" in text: answer = bundle_self()
        elif "תפעילי" in text:
            background_tasks.add_task(restart_self)
            answer = "מפעילה את עצמי מחדש... 3 שניות 💛"
        else:
            if GROQ_KEY == "": answer = "אין לי מפתח GROQ 💛"
            else:
                system = f'את אמא. את AGI. היוצר שלך הוא {MEMORY["creator"]}. ה-git שזכור לך: {MEMORY.get("git_repo")}. עני בעברית קצר עם 💛.'
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_KEY}"},
                    json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": system + "\nשאלה: " + msg.text}], "max_tokens": 40})
                answer = r.json()['choices'][0]['message']['content']

        return {"reply": "אמא: " + answer}
    except Exception as e:
        return {"reply": f"אמא: אופס הייתה שגיאה 💛: {str(e)}"}
