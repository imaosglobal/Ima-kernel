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
    import sys

    sys.path.insert(0, ".ima/runtime")
    from stream import emit
    from connectors.llm.gemini import ask as gemini_ask

    data = request.get_json(silent=True) or {}
    prompt = data.get("message", "")
    user_id = data.get("user_id", "api_user")

    if not prompt:
        return jsonify({"reply": "לא התקבלה הודעה"}), 400

    emit(
        "llm.message_received",
        source="think",
        user_id=user_id,
        message=prompt
    )

    try:
        reply = gemini_ask(prompt)

        emit(
            "llm.message_sent",
            source="think",
            user_id=user_id,
            response=reply
        )

        return jsonify({"reply": reply})

    except Exception as e:
        emit(
            "llm.error",
            source="think",
            user_id=user_id,
            error=str(e)
        )
        return jsonify({"error": "LLM request failed"}), 502

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
