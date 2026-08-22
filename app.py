from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json, os

# Load local .env without printing secrets.
env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key and key not in os.environ:
                os.environ[key] = value.strip().strip('"').strip("'")

import ima_master_runtime
from api.auth.google_oauth import google_auth

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not configured")

CORS(
    app,
    supports_credentials=True,
    origins=os.environ.get("FRONTEND_URL", "*")
)

app.register_blueprint(google_auth)

MEMORY_FILE = "unified_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE, "r"))
    return {"chats": [], "users": {}}

def save_memory(mem):
    from ima_canonical_memory_adapter import save_memory as _save
    return _save(mem)

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
    from connectors.llm.groq import ask as groq_ask

    data = request.get_json(silent=True) or {}
    prompt = data.get("message", "")

    if not prompt:
        return jsonify({"reply": "לא התקבלה הודעה"}), 400

    # Authenticated Google identity takes precedence over a client-supplied ID.
    user_id = session.get("user_id") or data.get("user_id", "api_user")

    mem = load_memory()
    if "users" not in mem:
        mem["users"] = {}

    user = mem["users"].setdefault(user_id, {})
    chats = user.setdefault("chats", [])

    # Build bounded per-user conversational context.
    recent = chats[-10:]

    context_lines = []
    for item in recent:
        context_lines.append(f"משתמש: {item.get('in', '')}")
        context_lines.append(f"אמא: {item.get('out', '')}")

    if context_lines:
        context = (
            "זהו ההקשר האחרון של השיחה עם המשתמש הזה בלבד. "
            "השתמש בו כדי לשמור על רציפות, אך אל תמציא מידע שלא מופיע בו.\n\n"
            + "\n".join(context_lines)
            + "\n\nהודעה חדשה של המשתמש:\n"
            + prompt
        )
    else:
        context = prompt

    emit(
        "llm.message_received",
        source="think",
        user_id=user_id,
        message=prompt
    )

    try:
        reply = gemini_ask(context)
        if reply.startswith("[gemini error"):
            reply = groq_ask(context)

        # Provider/API failures must never become conversational memory.
        if isinstance(reply, str) and reply.startswith("[gemini error:"):
            raise RuntimeError(reply)

        emit(
            "llm.message_sent",
            source="think",
            user_id=user_id,
            response=reply
        )

        mem["users"][user_id]["chats"].append({
            "in": prompt,
            "out": reply
        })
        save_memory(mem)

        return jsonify({"reply": reply})

    except Exception as e:
        emit(
            "llm.error",
            source="think",
            user_id=user_id,
            error=str(e)
        )
        return jsonify({"error": "LLM request failed"}), 502

@app.route("/knowledge/<domain>", methods=["GET"])
def knowledge(domain):
    from connectors.llm.gemini import ask as gemini_ask
    mem = load_memory()
    if "knowledge" not in mem:
        mem["knowledge"] = {}
    if domain in mem["knowledge"]:
        return jsonify({"domain": domain, "cached": True, "content": mem["knowledge"][domain]})

    prompt = f"תן סקירה מסודרת של תחום '{domain}': מה נצבר בו, מי האישים הבולטים (כולל רב-תחומיים שקישרו בינו לתחומים אחרים), ומה ההתפתחויות המשמעותיות ביותר."
    content_result = gemini_ask(prompt)
    if not content_result.startswith("[gemini error"):
        mem["knowledge"][domain] = content_result
        save_memory(mem)
    return jsonify({"domain": domain, "cached": False, "content": content_result})


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
