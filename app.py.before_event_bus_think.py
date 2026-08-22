from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os
import ima_master_runtime

app = Flask(__name__)
CORS(app)

MEMORY_FILE = "unified_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE, "r"))
    return {"chats": [], "users": {}}

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w"), ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return "IMA API is LIVE"

@app.route("/health")
def health():
    return jsonify({"ok": True})

@app.route("/brain", methods=["POST"])
def brain():
    data = request.get_json()
    msg = data.get("message", "")
    mem = load_memory()
    mem["chats"].append(msg)
    save_memory(mem)
    return jsonify({"reply": f"שמעתי: {msg}"})

@app.route("/ima", methods=["POST"])
def ima():
    data = request.json
    sender = data.get("sender", "guest")
    text = data.get("text", "")
    parts = text.split()
    if not parts:
        reply = "מה?"
    else:
        cmd = parts[0]
        if cmd == "חפש":
            reply = ima_master_runtime.ima_profile.ima_search(" ".join(parts[1:]), sender)
        elif cmd == "תהיי":
            reply = ima_master_runtime.ima_profile.request_form_change(sender, parts[1])
        elif cmd == "דודל":
            d = ima_master_runtime.ima_profile.get_today_doodle()
            reply = f"הדודל של היום: {d['form']} | סיבה: {d['reason']}"
        else:
            reply = "פקודות: חפש [מילה] | תהיי [צורה] | דודל"
    return jsonify({"reply": reply})



@app.route("/think", methods=["POST"])
def think():
    from connectors.llm.gemini import ask as gemini_ask
    data = request.json
    prompt = data.get("message", "")
    reply = gemini_ask(prompt)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
