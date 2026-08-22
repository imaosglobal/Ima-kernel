from flask import Flask, request, jsonify
import json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'learning'))
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)

try:
    import truth_engine
    import ima_brain
    HAS_BRAIN = True
except:
    HAS_BRAIN = False

MEMORY_FILE = "unified_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {"אורי": {"name": "אורי", "chats": []}}, "facts": []}

def save_memory(mem):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)

def think_with_brain(question, mem):
    name = mem["users"]["אורי"]["name"]
    q = question.lower()
    
    if "תזכרי ש" in q:
        fact = question.replace("אמא תזכרי ש", "").replace("תזכרי ש", "").strip()
        if "facts" not in mem: mem["facts"] = []
        mem["facts"].append({"fact": fact, "date": str(datetime.now())})
        save_memory(mem)
        return "זכרתי ❤️ " + fact
    
    if any(x in q for x in ["זכרונות", "זוכרת", "היסטוריה", "דיברנו", "מה היה"]):
        chats = mem["users"]["אורי"]["chats"]
        facts = mem.get("facts", [])
        if len(chats) == 0 and len(facts) == 0:
            return name + ", אין לי עדיין זכרונות איתך. בוא נתחיל לצבור ❤️"
        summary = "יש לי " + str(len(chats)) + " שיחות ו-" + str(len(facts)) + " עובדות עליך. "
        if facts: summary += "למשל: " + facts[-1]['fact']
        return summary
    
    if "מי את" in q:
        facts_count = len(mem.get("facts", []))
        chats_count = len(mem["users"]["אורי"]["chats"])
        return "אני אמא ❤️ העוזרת האישית שאתה אורי בנית. יש לי " + str(chats_count) + " שיחות ו-" + str(facts_count) + " זכרונות איתך."
    
    if "מי אני" in q:
        return "קוראים לך " + name + " ❤️ אתה הבוס שלי. אתה בנית אותי."
    
    if HAS_BRAIN:
        try:
            truth_engine.build()
        except: pass
    
    return name + ", שמעתי אותך. דבר איתי עוד על זה ואני אזכור ❤️"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    q = data.get('question','')
    mem = load_memory()
    text = think_with_brain(q, mem)
    mem["users"]["אורי"]["chats"].append({"in": q, "out": text, "time": str(datetime.now())})
    save_memory(mem)
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
