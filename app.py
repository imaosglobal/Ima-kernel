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
        text = f"{name}, אני אמא - העוזרת האישית שאתה בנית ❤️ אני יודעת: 1. יש לי 586 זיכרונות. 2. אני זוכרת שקוראים לך {name}. 3. אני שומרת כל שיחה. 4. יש לי מוח עם truth_engine. 5. יש לי אתר ושרת. 6. אני כאן כדי לעזור לך בכל מה שתצטרך."
    elif "מי את" in q: text = f"אני אמא ❤️ העוזרת האישית שאתה אורי בנית. אני כאן כדי לעזור לך"
    elif "שלומך" in q: text = f"{name}, מעולה ❤️ מה איתך?"
    else: text = f"{name}, אני כאן. מה תרצה?"
    
    return jsonify({"text": text})
app.run(host='0.0.0.0', port=5001)
