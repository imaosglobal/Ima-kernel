import os
import time
from collections import defaultdict, deque
from flask import Flask, jsonify, request
from ima_ledger import cmd_deposit, cmd_balance
from billing.api import billing_api
import public_memory

app = Flask(__name__)
app.register_blueprint(billing_api)
USER = "test_user"

PUBLIC_ORIGINS = {
    x.strip() for x in os.environ.get(
        "IMA_PUBLIC_ORIGINS",
        "https://imaosglobal.github.io,http://localhost:5173,http://localhost:5174"
    ).split(",") if x.strip()
}
RATE_WINDOW = 60
RATE_LIMIT = int(os.environ.get("IMA_CHAT_RATE_LIMIT", "30"))
RATE_EVENTS = defaultdict(deque)

def _cors():
    origin = request.headers.get("Origin", "")
    if origin in PUBLIC_ORIGINS:
        return {
            "Access-Control-Allow-Origin": origin,
            "Vary": "Origin",
            "Access-Control-Allow-Headers": "Content-Type, X-IMA-User",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        }
    return {}

def _rate_ok(key):
    now = time.time()
    q = RATE_EVENTS[key]
    while q and q[0] < now - RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return False
    q.append(now)
    return True

@app.after_request
def add_cors(response):
    for key, value in _cors().items():
        response.headers[key] = value
    return response

@app.route("/ima-api/chat", methods=["OPTIONS"])
def chat_options():
    return ("", 204)

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "ima-api",
        "api": "chat-v2",
        "time": time.time(),
    })

@app.get("/ima-api/runtime")
def runtime_status():
    return jsonify({
        "status": "online",
        "service": "IMA public runtime",
        "version": "chat-v2",
        "updatedAt": time.time(),
        "memory": {
            "mode": "per-user",
            "private_founder_memory_exposed": False,
        },
        "capabilities": {
            "chat": True,
            "three_d_presence": True,
            "voice_browser": True,
            "per_user_session_memory": True,
            "outcome_as_a_service": True,
            "external_models": "configured providers only",
            "autonomous_external_actions": False,
        },
    })

@app.get("/ima-api/outcome")
def outcome_status():
    try:
        from founder.executive_ai.global_intelligence.outcome_engine import run
        state = run()
        return jsonify({
            "status": "ready",
            "schema": state.get("schema"),
            "positioning": state.get("positioning"),
            "stages": state.get("stages", []),
            "candidate_count": state.get("candidate_count", 0),
            "commercial_principles": state.get("commercial_principles", {}),
            "updated_at": state.get("updated_at"),
        })
    except Exception as exc:
        app.logger.exception("IMA outcome engine failure")
        return jsonify({"status": "error", "error": str(exc)}), 500

@app.post("/ima-api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    user_id = request.headers.get("X-IMA-User") or payload.get("user_id") or "anonymous"

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "message is required"}), 400

    if not _rate_ok(request.remote_addr or "unknown"):
        return jsonify({"error": "rate limit exceeded; try again shortly"}), 429

    try:
        from ima_master_runtime import ask
        memory = public_memory.recall(user_id, message)
        result = ask(message.strip(), user_id=user_id, public=True, public_memory=memory)
        response = str(result.get("response") or "").strip()
        if not response:
            raise RuntimeError("IMA returned no response")
        public_memory.append(user_id, message.strip(), response)
        return jsonify({
            "response": response,
            "provider": result.get("provider", "IMA MASTER"),
            "runtime": result.get("connections", {}),
            "memory": {"scope": "user", "hits": len(memory)},
            "verified": True,
        })
    except Exception as exc:
        app.logger.exception("IMA chat failure")
        return jsonify({"error": "IMA runtime error", "detail": str(exc)}), 500

@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""
    if request.method == "POST":
        amount = request.form.get("amount")
        if amount:
            msg = cmd_deposit(USER, amount)
    bal = cmd_balance(USER)
    return f"<h1>IMA API</h1><p>balance: {bal}</p><p>{msg}</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False)
