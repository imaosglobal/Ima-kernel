import hashlib
import hmac
import json
import os
import secrets
import time
from collections import defaultdict, deque
from flask import Flask, jsonify, request
from ima_ledger import cmd_deposit, cmd_balance
from billing.api import billing_api
import public_memory
import requests

try:
    from integrations import nylas_email
except Exception:
    nylas_email = None

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
NYLAS_WEBHOOK_EVENTS = deque(maxlen=500)
NYLAS_WEBHOOK_SECRET = os.environ.get("NYLAS_WEBHOOK_SECRET", "").strip()
NYLAS_WEBHOOK_SETUP_TOKEN = os.environ.get("NYLAS_WEBHOOK_SETUP_TOKEN", "").strip()
NYLAS_WEBHOOK_URL = os.environ.get("NYLAS_WEBHOOK_URL", "https://ima-915m.onrender.com/ima-api/webhooks/nylas")
SESSION_SECRET = os.environ.get("IMA_SESSION_SECRET") or secrets.token_hex(32)


def _issue_session():
    user_id = secrets.token_urlsafe(24)
    signature = hmac.new(
        SESSION_SECRET.encode(), user_id.encode(), hashlib.sha256
    ).hexdigest()
    return f"{user_id}.{signature}"


def _session_user_id():
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return None
    token = authorization[7:].strip()
    if "." not in token:
        return None
    user_id, signature = token.rsplit(".", 1)
    if not user_id or not signature:
        return None
    expected = hmac.new(
        SESSION_SECRET.encode(), user_id.encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return None
    return "public:" + user_id

def _cors():
    origin = request.headers.get("Origin", "")
    if origin in PUBLIC_ORIGINS:
        return {
            "Access-Control-Allow-Origin": origin,
            "Vary": "Origin",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
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

@app.route("/ima-api/session", methods=["GET", "OPTIONS"])
def session():
    if request.method == "OPTIONS":
        return ("", 204)
    return jsonify({"token": _issue_session(), "scope": "public-user"})

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

@app.get("/ima-api/email/status")
def email_status():
    if nylas_email is None:
        return jsonify({"provider": "nylas", "configured": False, "status": "integration_unavailable"}), 503
    state = nylas_email.status()
    return jsonify({**state, "status": "ready" if state["configured"] else "awaiting_secret"})


@app.get("/ima-api/email/verify")
def email_verify():
    """Verify backend-to-Nylas mailbox access without returning message content."""
    if nylas_email is None:
        return jsonify({"provider": "nylas", "verified": False, "status": "integration_unavailable"}), 503
    if not _rate_ok("email-verify:" + (request.remote_addr or "unknown")):
        return jsonify({"error": "verification rate limit exceeded; try again shortly"}), 429
    try:
        state = nylas_email.status()
        if not state.get("configured"):
            return jsonify({"provider": "nylas", "verified": False, "status": "awaiting_secret"}), 503
        result = nylas_email.list_messages(limit=1, unread=None)
        data = result.get("data", [])
        return jsonify({
            "provider": "nylas",
            "mailbox": state.get("mailbox"),
            "verified": True,
            "message_count_checked": len(data),
            "status": "ready",
        })
    except requests.HTTPError as exc:
        app.logger.exception("Nylas mailbox verification failed")
        return jsonify({"provider": "nylas", "verified": False, "status": "mailbox_request_failed", "status_code": exc.response.status_code}), 502
    except Exception:
        app.logger.exception("Nylas mailbox verification failed")
        return jsonify({"provider": "nylas", "verified": False, "status": "mailbox_request_failed"}), 502


def _nylas_signature_valid(raw_body):
    if not NYLAS_WEBHOOK_SECRET:
        return False
    provided = request.headers.get("X-Nylas-Signature", "") or request.headers.get("x-nylas-signature", "")
    if not provided:
        return False
    expected = hmac.new(
        NYLAS_WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(provided, expected)


@app.route("/ima-api/webhooks/nylas", methods=["GET", "POST"])
def nylas_webhook():
    if request.method == "GET":
        challenge = request.args.get("challenge")
        if not challenge:
            return ("missing challenge", 400)
        return challenge, 200, {"Content-Type": "text/plain; charset=utf-8"}

    raw_body = request.get_data(cache=False)
    if not _nylas_signature_valid(raw_body):
        return jsonify({"error": "invalid Nylas webhook signature"}), 401

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except Exception:
        return jsonify({"error": "invalid JSON"}), 400

    notification = payload.get("data", {}) if isinstance(payload, dict) else {}
    event_type = notification.get("type") or payload.get("type") or "unknown"
    event_data = notification.get("object") or notification.get("data") or {}
    event_id = payload.get("id") or notification.get("id") or ""
    NYLAS_WEBHOOK_EVENTS.append({
        "received_at": time.time(),
        "type": event_type,
        "id": event_id,
        "grant_id_present": bool(event_data.get("grant_id") or payload.get("grant_id")),
        "message_id": event_data.get("id") if event_type.startswith("message.") else None,
        "thread_id": event_data.get("thread_id") if event_type.startswith("message.") else None,
    })
    app.logger.info("Nylas webhook received type=%s id=%s", event_type, event_id)
    return jsonify({"received": True, "type": event_type}), 200


@app.get("/ima-api/email/monitor")
def email_monitor_status():
    events = list(NYLAS_WEBHOOK_EVENTS)
    return jsonify({
        "provider": "nylas",
        "mode": "webhook",
        "configured": bool(NYLAS_WEBHOOK_SECRET),
        "endpoint": NYLAS_WEBHOOK_URL,
        "events_buffered": len(events),
        "last_event": events[-1] if events else None,
        "verified_signature": bool(NYLAS_WEBHOOK_SECRET),
    })


@app.post("/ima-api/email/webhook/setup")
def email_webhook_setup():
    if not NYLAS_WEBHOOK_SETUP_TOKEN or request.headers.get("X-IMA-Setup-Token") != NYLAS_WEBHOOK_SETUP_TOKEN:
        return jsonify({"error": "setup authorization required"}), 401
    if not nylas_email or not nylas_email.configured():
        return jsonify({"error": "Nylas integration is not configured"}), 503
    try:
        trigger_types = ["message.created", "grant.expired"]
        response = requests.post(
            f"{nylas_email.BASE_URL}/webhooks",
            headers={"Authorization": f"Bearer {nylas_email.API_KEY}", "Content-Type": "application/json", "Accept": "application/json"},
            json={"trigger_types": trigger_types, "description": "IMA continuous email monitor", "webhook_url": NYLAS_WEBHOOK_URL, "webhook_secret": NYLAS_WEBHOOK_SECRET},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json().get("data", {})
        return jsonify({
            "created": True,
            "id": data.get("id"),
            "status": data.get("status"),
            "trigger_types": data.get("trigger_types"),
            "webhook_secret": data.get("webhook_secret"),
        })
    except requests.HTTPError as exc:
        app.logger.exception("Nylas webhook setup failed")
        return jsonify({"created": False, "status_code": exc.response.status_code, "error": "Nylas webhook setup failed"}), 502
    except Exception:
        app.logger.exception("Nylas webhook setup failed")
        return jsonify({"created": False, "error": "Nylas webhook setup failed"}), 502


@app.get("/ima-api/email/messages")
def email_messages():
    if nylas_email is None:
        return jsonify({"error": "Nylas integration unavailable"}), 503
    if not _session_user_id():
        return jsonify({"error": "valid IMA session required"}), 401
    try:
        limit = request.args.get("limit", "20")
        unread = request.args.get("unread")
        unread_value = None if unread is None else unread.lower() == "true"
        result = nylas_email.list_messages(limit=limit, unread=unread_value)
        return jsonify({
            "provider": "nylas",
            "mailbox": nylas_email.status()["mailbox"],
            "data": result.get("data", []),
            "next_cursor": result.get("next_cursor"),
            "verified": True,
        })
    except requests.HTTPError as exc:
        app.logger.exception("Nylas message fetch failed")
        return jsonify({"error": "Nylas mailbox request failed", "status_code": exc.response.status_code}), 502
    except Exception:
        app.logger.exception("Nylas message fetch failed")
        return jsonify({"error": "Nylas mailbox request failed"}), 502


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
        return jsonify({"status": "error", "error": "IMA outcome engine unavailable"}), 500

@app.post("/ima-api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    user_id = _session_user_id()

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "message is required"}), 400

    if not user_id:
        return jsonify({"error": "valid IMA session required"}), 401

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
        return jsonify({"error": "IMA runtime error"}), 500

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
