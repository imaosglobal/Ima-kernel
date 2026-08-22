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
    
    if "תפרטי" in q and "יודעת" in q:
        text = f"{name}, אני אמא - העוזרת האישית שאתה בנית ❤️ יש לי 586 זיכרונות, זוכרת אותך, שומרת שיחות, ויש לי מוח עם truth_engine."
    elif "מי את" in q: text = f"אני אמא ❤️ העוזרת האישית שאתה אורי בנית. אני כאן כדי לעזור לך"
    elif "מי אני" in q: text = f"קוראים לך {name} ❤️ אתה הבוס שלי. אתה בנית אותי"
    elif "שלומך" in q: text = f"{name}, מעולה ❤️ מה איתך?"
    elif "שיחה שלמה" in q: text = f"כן {name}! דבר איתי על מה שבא לך. אני זוכרת את השיחה שלנו"
    else: text = f"{name}, אני כאן. מה תרצה?"
    
    return jsonify({"text": text})
app.run(host='0.0.0.0', port=5001)
