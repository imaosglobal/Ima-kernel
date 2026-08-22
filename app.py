from flask import Flask, request, jsonify
import json, os
app = Flask(__name__)

def load_unified():
    if os.path.exists("unified_memory.json"):
        with open("unified_memory.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {"אורי": {"name": "אורי", "chats": []}}}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    q = data.get('question','')
    mem = load_unified()
    name = mem["users"]["אורי"]["name"]
    
    if "שלומך" in q: text = f"{name}, מעולה ❤️ מה איתך?"
    elif "מי את" in q: text = "אני אמא שלך ❤️ כאן כדי לשמור עליך ולעזור בכל מה שתצטרך"
    elif "זוכרת" in q and "שם" in q: text = f"ברור שאני זוכרת ❤️ קוראים לך {name}"
    else: text = f"{name}, אני כאן. מה תרצה?"
    
    return jsonify({"text": text})
app.run(host='0.0.0.0', port=5001)
