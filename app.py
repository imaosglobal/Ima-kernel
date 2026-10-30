import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import time
from collections import defaultdict, deque
from flask import Flask, jsonify, request
from ima_ledger import cmd_deposit, cmd_balance
from billing.api import billing_api
import public_memory
import requests
import importlib.util

try:
    from integrations import nylas_email
except Exception:
    nylas_email = None

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("IMA_FLASK_SECRET") or os.environ.get("IMA_SESSION_SECRET") or secrets.token_hex(32)
app.register_blueprint(billing_api)
try:
    from api.auth.google_oauth import google_auth
    app.register_blueprint(google_auth)
except Exception:
    google_auth = None
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

REGISTRY_PATH = Path(__file__).resolve().parent / ".ima" / "plugins" / "REGISTRY.json"
UNIVERSAL_MEMORY_PATH = Path(__file__).resolve().parent / ".ima" / "memory" / "universal_interaction_memory.py"

def _universal_memory():
    spec = importlib.util.spec_from_file_location("ima_universal_interaction_memory", UNIVERSAL_MEMORY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("universal interaction memory unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _registry_provider_status(provider: str) -> str:
    """Return registry status for a provider; unknown providers are not executable."""
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        for item in registry.get("connected", []):
            if item.get("provider") == provider:
                return item.get("status", "connected")
    except Exception:
        app.logger.exception("IMA capability registry read failed")
    return "unknown"


def _provider_execution_allowed(provider: str) -> bool:
    return _registry_provider_status(provider) == "connected"



def _issue_session(user_id=None):
    user_id = user_id or secrets.token_urlsafe(24)
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
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        }
    if origin == "null" and request.path == "/ima-api/auth/config":
        return {
            "Access-Control-Allow-Origin": "null",
            "Vary": "Origin",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
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

@app.get("/ima-api/auth/config")
def auth_config():
    return jsonify({
        "google": {
            "enabled": bool(os.environ.get("GOOGLE_CLIENT_ID", "").strip()),
            "client_id": os.environ.get("GOOGLE_CLIENT_ID", "").strip() or None,
        },
        "memory": "consent-based",
    })

@app.post("/ima-api/auth/google")
def google_auth():
    payload = request.get_json(silent=True) or {}
    credential = str(payload.get("credential") or "").strip()
    expected_nonce = str(payload.get("nonce") or "").strip()
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip()
    if not credential or not client_id:
        return jsonify({"error": "Google sign-in is not configured"}), 503
    try:
        response = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": credential}, timeout=10)
        response.raise_for_status()
        claims = response.json()
        if claims.get("aud") != client_id:
            return jsonify({"error": "Google credential audience mismatch"}), 401
        if claims.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
            return jsonify({"error": "Google credential issuer mismatch"}), 401
        if int(claims.get("exp", "0")) <= int(time.time()):
            return jsonify({"error": "Google credential expired"}), 401
        if expected_nonce and claims.get("nonce") != expected_nonce:
            return jsonify({"error": "Google credential nonce mismatch"}), 401
        subject = claims.get("sub")
        if not subject:
            return jsonify({"error": "Google credential missing subject"}), 401
        user_id = "google:" + subject
        return jsonify({"token": _issue_session(user_id), "scope": "google-user", "user": {"id": user_id, "name": claims.get("name"), "email": claims.get("email"), "picture": claims.get("picture"), "email_verified": claims.get("email_verified") == "true"}})
    except requests.HTTPError:
        return jsonify({"error": "Google credential could not be verified"}), 401
    except Exception:
        app.logger.exception("Google authentication failed")
        return jsonify({"error": "Google authentication unavailable"}), 502

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

@app.route("/ima-api/memory/consent", methods=["GET", "PUT", "OPTIONS"])
def memory_consent():
    if request.method == "OPTIONS":
        return ("", 204)
    user_id = _session_user_id()
    if not user_id:
        return jsonify({"error": "valid IMA session required"}), 401
    try:
        memory = _universal_memory()
        if request.method == "GET":
            return jsonify({"scope": "user", "consent": memory.get_consent(user_id)})
        payload = request.get_json(silent=True) or {}
        result = memory.set_consent(user_id, payload.get("status"), source="public-runtime")
        return jsonify({"scope": "user", "consent": result})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Universal memory consent operation failed")
        return jsonify({"error": "universal memory consent unavailable"}), 503

@app.get("/ima-api/memory/export")
def memory_export():
    user_id = _session_user_id()
    if not user_id:
        return jsonify({"error": "valid IMA session required"}), 401
    try:
        memory = _universal_memory()
        return jsonify({"scope": "user", "records": memory.export_user_memory(user_id), "consent": memory.get_consent(user_id)})
    except Exception:
        app.logger.exception("Universal memory export failed")
        return jsonify({"error": "universal memory export unavailable"}), 503

@app.delete("/ima-api/memory")
def memory_delete():
    user_id = _session_user_id()
    if not user_id:
        return jsonify({"error": "valid IMA session required"}), 401
    try:
        memory = _universal_memory()
        deleted = memory.delete_user_memory(user_id)
        memory.set_consent(user_id, "DENIED", source="public-runtime-delete")
        return jsonify({"deleted": deleted, "scope": "user", "consent": memory.get_consent(user_id)})
    except Exception:
        app.logger.exception("Universal memory deletion failed")
        return jsonify({"error": "universal memory deletion unavailable"}), 503

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
            "universal_interaction_memory": True,
            "universal_memory_requires_consent": True,
            "outcome_as_a_service": True,
            "external_models": "configured providers only",
            "autonomous_external_actions": False,
        },
    })

@app.get("/ima-api/email/status")
def email_status():
    if not _provider_execution_allowed("Nylas"):
        return jsonify({"provider": "nylas", "configured": False, "status": "candidate_not_connected", "execution_allowed": False}), 503
    if nylas_email is None:
        return jsonify({"provider": "nylas", "configured": False, "status": "integration_unavailable"}), 503
    state = nylas_email.status()
    return jsonify({**state, "status": "ready" if state["configured"] else "awaiting_secret"})


@app.get("/ima-api/email/verify")
def email_verify():
    """Verify backend-to-Nylas mailbox access without returning message content."""
    if not _provider_execution_allowed("Nylas"):
        return jsonify({"provider": "nylas", "verified": False, "status": "candidate_not_connected", "execution_allowed": False}), 503
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
    if not _provider_execution_allowed("Nylas"):
        return jsonify({"provider": "nylas", "mode": "webhook", "configured": False, "verified_signature": False, "events_buffered": 0, "last_event": None, "status": "candidate_not_connected", "execution_allowed": False}), 503
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


@app.route("/ima-api/email/webhook/setup", methods=["GET", "POST"])
def email_webhook_setup():
    if not _provider_execution_allowed("Nylas"):
        return jsonify({"provider": "nylas", "created": False, "status": "candidate_not_connected", "execution_allowed": False}), 503
    setup_token = request.headers.get("X-IMA-Setup-Token", "") or request.args.get("token", "")
    if not NYLAS_WEBHOOK_SETUP_TOKEN or setup_token != NYLAS_WEBHOOK_SETUP_TOKEN:
        return jsonify({"error": "setup authorization required"}), 401
    if not nylas_email or not nylas_email.configured():
        return jsonify({"error": "Nylas integration is not configured"}), 503
    try:
        trigger_types = ["message.created"]
        response = requests.post(
            f"{nylas_email.BASE_URL}/webhooks",
            headers={"Authorization": f"Bearer {nylas_email.API_KEY}", "Content-Type": "application/json", "Accept": "application/json"},
            json={"trigger_types": trigger_types, "description": "IMA continuous email monitor", "webhook_url": NYLAS_WEBHOOK_URL},
            timeout=45,
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
        return jsonify({"created": False, "status_code": exc.response.status_code, "error": "Nylas webhook setup failed", "provider_error": (exc.response.text or "")[:500]}), 502
    except Exception:
        app.logger.exception("Nylas webhook setup failed")
        return jsonify({"created": False, "error": "Nylas webhook setup failed"}), 502


@app.get("/ima-api/email/messages")
def email_messages():
    if not _provider_execution_allowed("Nylas"):
        return jsonify({"provider": "nylas", "data": [], "verified": False, "status": "candidate_not_connected", "execution_allowed": False}), 503
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


@app.route("/ima-api/direction", methods=["GET", "PUT", "OPTIONS"])
def direction_map():
    """User-owned vocation/direction map. Nothing is inferred or shared automatically."""
    if request.method == "OPTIONS":
        return ("", 204)
    user_id = _session_user_id()
    if not user_id:
        return jsonify({"error": "valid IMA session required"}), 401
    from learning import direction_map as dm
    if request.method == "GET":
        return jsonify({"direction_map": dm.get(user_id), "ownership": "user-controlled", "shared": False})
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "direction_map object is required"}), 400
    try:
        return jsonify({"direction_map": dm.replace(user_id, payload), "ownership": "user-controlled", "shared": False})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.route("/ima-api/direction/entry", methods=["POST", "DELETE", "OPTIONS"])
def direction_entry():
    if request.method == "OPTIONS":
        return ("", 204)
    user_id = _session_user_id()
    if not user_id:
        return jsonify({"error": "valid IMA session required"}), 401
    from learning import direction_map as dm
    payload = request.get_json(silent=True) or {}
    category = payload.get("category")
    if request.method == "POST":
        try:
            result = dm.add_entry(user_id, category, payload.get("entry"))
            return jsonify({"direction_map": result, "ownership": "user-controlled"}), 201
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
    try:
        removed, result = dm.delete_entry(user_id, category, payload.get("entry_id"))
        return jsonify({"deleted": removed, "direction_map": result}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

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

@app.get("/ima-api/age/status")
def age_assurance_status():
    """Expose age-assurance readiness without exposing secrets or user data."""
    configured = bool(
        os.environ.get("IMA_AGE_ATTESTATION_SECRET")
        and os.environ.get("IMA_AGE_ISSUER")
    )
    return jsonify({
        "status": "ready" if configured else "not_configured",
        "method": "trusted_signed_age_attestation",
        "audience": os.environ.get("IMA_AGE_AUDIENCE", "ima-public-chat"),
        "verified_age_signal_available": configured,
        "fallback": "protective_unknown_age",
        "exact_birth_date_collected": False,
    })


@app.post("/ima-api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    user_id = _session_user_id()

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "message is required"}), 400

    if not user_id or not user_id.startswith("public:google:"):
        return jsonify({"error": "verified Google sign-in required"}), 401

    if not _rate_ok(request.remote_addr or "unknown"):
        return jsonify({"error": "rate limit exceeded; try again shortly"}), 429

    try:
        from ima_master_runtime import ask
        universal = _universal_memory()
        consent = universal.get_consent(user_id)
        memory = public_memory.recall(user_id, message) if consent.get("status") == "GRANTED" else []
        personalization = payload.get("personalization") if isinstance(payload.get("personalization"), dict) else {}
        result = ask(message.strip(), user_id=user_id, public=True, public_memory=memory, personalization=personalization)
        response = str(result.get("response") or "").strip()
        if not response:
            raise RuntimeError("IMA returned no response")

        # Accept only a short-lived signed attestation from the configured trusted
        # issuer, bound to this authenticated session. Never trust a raw client age.
        from learning.age_assurance import verify_age_attestation
        from learning.child_safety_engine import enforce_response
        age_signal = verify_age_attestation(payload.get("age_attestation"), user_id)
        age_band = age_signal["age_band"] if age_signal.get("verified") else "unknown"
        language = "he" if any("\\u0590" <= char <= "\\u05FF" for char in message) else "en"
        safety = enforce_response(
            age_band=age_band,
            user_message=message.strip(),
            assistant_response=response,
            language=language,
        )
        response = safety["response"].strip()
        if not response:
            raise RuntimeError("IMA safety layer returned no response")

        # Store only the final response after the first-pass safety screen.
        if consent.get("status") == "GRANTED":
            public_memory.append(user_id, message.strip(), response)
        try:
            if consent.get("status") == "GRANTED":
                universal.capture(
                    user_id=user_id,
                    source="ima-api/chat",
                    content=message.strip(),
                    consent="GRANTED",
                    language=language,
                    interface="public-web-chat",
                    outcome=response,
                    verification="first-pass-safety-screen",
                    temporal_class="PRESENT",
                    authorized_learning=False,
                    status="VERIFIED",
                )
        except ValueError as exc:
            app.logger.warning("Universal memory capture skipped: %s", exc)
        except Exception:
            app.logger.exception("Universal memory capture failed")
        return jsonify({
            "response": response,
            "provider": result.get("provider", "IMA MASTER"),
            "runtime": result.get("connections", {}),
            "memory": {"scope": "user", "hits": len(memory)},
            "verified": True,
            "safety": {
                "screened": True,
                "policy_version": safety.get("policy_version"),
                "age_band": safety.get("age_band", "unknown"),
                "protective_mode": safety.get("protective_mode", True),
                "age_assurance": {
                    "verified": bool(age_signal.get("verified")),
                    "status": age_signal.get("status", "unknown"),
                    "age_band": age_band,
                },
                "risk_codes": safety.get("risk_codes", []),
                "response_action": safety.get("response_action"),
                "limitations": safety.get("limitations"),
            },
        })
    except Exception as exc:
        app.logger.exception("IMA chat failure")
        return jsonify({"error": "IMA runtime error"}), 500

@app.get("/ima-api/capabilities/gaps")
def capability_gaps():
    """Expose the canonical capability-gap queue and next prioritized gap."""
    try:
        import importlib.util
        module_path = Path(__file__).resolve().parent / ".ima" / "plugins" / "gap_queue.py"
        spec = importlib.util.spec_from_file_location("ima_gap_queue", module_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("gap queue module spec unavailable")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return jsonify(module.CapabilityGapQueue().snapshot())
    except Exception:
        app.logger.exception("IMA capability gap queue failure")
        return jsonify({"error": "capability gap queue unavailable"}), 500


@app.get("/ima-api/capabilities")
def capabilities():
    """Expose the canonical capability map plus executable runtime routing state."""
    try:
        path = Path(__file__).resolve().parent / ".ima" / "plugins" / "REGISTRY.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        import importlib.util
        runtime_path = Path(__file__).resolve().parent / ".ima" / "plugins" / "capability_runtime.py"
        spec = importlib.util.spec_from_file_location("ima_capability_runtime_api", runtime_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("capability runtime module spec unavailable")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        runtime = module.snapshot()
        return jsonify({
            "schema_version": registry.get("schema_version"),
            "policy": registry.get("policy", {}),
            "routing": registry.get("routing", {}),
            "providers": [
                {
                    "id": item.get("id"),
                    "provider": item.get("provider"),
                    "status": item.get("status", "connected"),
                    "capabilities": item.get("capabilities", []),
                }
                for item in registry.get("connected", [])
            ],
            "runtime": runtime,
            "verified_source": ".ima/plugins/REGISTRY.json + .ima/plugins/capability_runtime.py",
        })
    except Exception:
        app.logger.exception("IMA capability registry failure")
        return jsonify({"error": "capability registry unavailable"}), 500


@app.get("/ima-api/capabilities/<capability>")
def capability_route(capability):
    """Return provider routing truth for one capability without executing it."""
    try:
        import importlib.util
        runtime_path = Path(__file__).resolve().parent / ".ima" / "plugins" / "capability_runtime.py"
        spec = importlib.util.spec_from_file_location("ima_capability_runtime_route", runtime_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("capability runtime module spec unavailable")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return jsonify(module.route(capability))
    except Exception:
        app.logger.exception("IMA capability route failure")
        return jsonify({"error": "capability route unavailable"}), 500


# --- Real-user growth, feedback and reputation instrumentation ---
GROWTH_DIR = Path(__file__).resolve().parent / ".ima" / "growth"
FEEDBACK_QUEUE = GROWTH_DIR / "feedback.runtime.jsonl"
EVENT_QUEUE = GROWTH_DIR / "events.runtime.jsonl"
FEEDBACK_ARCHIVE_DIR = GROWTH_DIR / "feedback_archive"
FEEDBACK_LEARNING_DIR = GROWTH_DIR / "feedback_learning"

def _utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _feedback_archive_path(epoch=None):
    stamp = time.gmtime(epoch if epoch is not None else time.time())
    return FEEDBACK_ARCHIVE_DIR / f"feedback-{time.strftime('%Y-%m-%d', stamp)}.jsonl"

def _feedback_learning_path(epoch=None):
    stamp = time.gmtime(epoch if epoch is not None else time.time())
    return FEEDBACK_LEARNING_DIR / f"learning-{time.strftime('%Y-%m-%d', stamp)}.jsonl"

def _derive_feedback_lesson(sentiment, text):
    lowered = text.lower()
    tags = []
    if sentiment == "problem":
        tags.append("bug")
    if sentiment == "improvement":
        tags.append("feature_request")
    if any(x in lowered for x in ["לא עובד", "לא עובדת", "תקוע", "תקועה", "שגיאה", "error", "broken"]):
        tags.append("reliability")
    if any(x in lowered for x in ["גוגל", "google", "כניסה", "login"]):
        tags.append("authentication")
    if any(x in lowered for x in ["משוב", "feedback"]):
        tags.append("feedback_loop")
    if any(x in lowered for x in ["התקנה", "install", "מסך הבית"]):
        tags.append("installation")
    if any(x in lowered for x in ["קישור", "לינק", "link"]):
        tags.append("navigation")
    if any(x in lowered for x in ["איטי", "מהיר", "טעינה", "טוען"]):
        tags.append("performance")
    if not tags:
        tags.append("general")
    lesson = {
        "action": "investigate_and_verify" if sentiment in {"problem", "not_useful"} else "evaluate_and_prioritize",
        "tags": sorted(set(tags)),
        "source_sentiment": sentiment,
        "summary": text[:500],
        "applied_automatically": False,
    }
    return lesson
POSTHOG_HOST = os.environ.get("POSTHOG_HOST", "").strip().rstrip("/")
POSTHOG_API_KEY = os.environ.get("POSTHOG_API_KEY", "").strip()

def _growth_identity():
    """Return a privacy-preserving event identity; never store raw email."""
    uid = _session_user_id()
    if uid:
        return "user_" + hashlib.sha256(uid.encode()).hexdigest()[:24]
    anon = request.headers.get("X-IMA-Anonymous-ID", "").strip()
    if anon:
        return "anon_" + hashlib.sha256(anon.encode()).hexdigest()[:24]
    return "anon_session_" + hashlib.sha256((request.remote_addr or "unknown").encode()).hexdigest()[:24]

def _posthog_capture(event_name, properties):
    if not POSTHOG_HOST or not POSTHOG_API_KEY:
        return {"sent": False, "status": "not_configured"}
    payload = {
        "api_key": POSTHOG_API_KEY,
        "event": event_name,
        "distinct_id": _growth_identity(),
        "properties": {**properties, "product": "IMA", "schema": "IMA-GROWTH-1.0"},
    }
    response = requests.post(
        f"{POSTHOG_HOST}/capture/",
        json=payload,
        timeout=8,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return {"sent": True, "status": "accepted"}

def _queue_runtime(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

@app.post("/ima-api/analytics")
def analytics_event():
    payload = request.get_json(silent=True) or {}
    event = str(payload.get("event") or "").strip()
    allowed = {
        "page_view", "chat_started", "chat_completed", "share_clicked",
        "feedback_opened", "feedback_submitted", "install_prompt",
        "pwa_installed", "rating_prompt_shown", "rating_clicked",
        "language_changed", "onboarding_completed",
    }
    if event not in allowed:
        return jsonify({"error": "unsupported event"}), 400
    properties = payload.get("properties")
    if not isinstance(properties, dict):
        properties = {}
    safe = {
        str(k)[:64]: str(v)[:256]
        for k, v in properties.items()
        if k not in {"email", "name", "message", "text", "token", "credential"}
    }
    record = {
        "time": time.time(),
        "event": event,
        "identity": _growth_identity(),
        "properties": safe,
    }
    try:
        provider = _posthog_capture(event, safe)
        if not provider["sent"]:
            _queue_runtime(EVENT_QUEUE, record)
        return jsonify({"accepted": True, "provider": provider["status"]})
    except Exception:
        app.logger.exception("IMA analytics provider failed")
        _queue_runtime(EVENT_QUEUE, record)
        return jsonify({"accepted": True, "provider": "runtime_queue"})

@app.post("/ima-api/feedback")
def feedback():
    payload = request.get_json(silent=True) or {}
    sentiment = str(payload.get("sentiment") or "").strip()
    text = str(payload.get("text") or "").strip()
    language = str(payload.get("language") or "unknown").strip()[:16]
    allowed = {"useful", "not_useful", "problem", "improvement"}
    if sentiment not in allowed:
        return jsonify({"error": "invalid feedback type"}), 400
    if not text or len(text) > 4000:
        return jsonify({"error": "feedback text is required and must be <= 4000 characters"}), 400

    received_epoch = time.time()
    user_id = _session_user_id()
    auth_state = "google_authenticated" if user_id and user_id.startswith("public:google:") else "anonymous"
    client_timezone = str(payload.get("timezone") or "unknown")[:80]
    client_now = str(payload.get("client_time") or "")[:80]
    page = str(payload.get("page") or "")[:1000]
    referrer = str(payload.get("referrer") or "")[:1000]
    user_agent = request.headers.get("User-Agent", "")[:1000]
    archive_record = {
        "received_at": _utc_now(),
        "received_epoch": received_epoch,
        "date_utc": time.strftime("%Y-%m-%d", time.gmtime(received_epoch)),
        "hour_utc": int(time.strftime("%H", time.gmtime(received_epoch))),
        "sentiment": sentiment,
        "language": language,
        "text": text,
        "identity": _growth_identity(),
        "auth_state": auth_state,
        "page": page,
        "referrer": referrer,
        "client_timezone": client_timezone,
        "client_time": client_now,
        "user_agent": user_agent,
        "source": "public-runtime",
    }

    lesson = _derive_feedback_lesson(sentiment, text)
    archive_record["lesson"] = lesson

    # Always append to the current runtime archive and a date-partitioned archive.
    try:
        _queue_runtime(FEEDBACK_QUEUE, archive_record)
        _queue_runtime(_feedback_archive_path(received_epoch), archive_record)
        _queue_runtime(_feedback_learning_path(received_epoch), {
            "received_at": archive_record["received_at"],
            "feedback_date_utc": archive_record["date_utc"],
            "feedback_id": archive_record["identity"] + ":" + str(int(received_epoch * 1000)),
            "lesson": lesson,
        })
        stored_runtime = True
    except Exception:
        app.logger.exception("IMA feedback archive write failed")
        stored_runtime = False

    analytics = {"sent": False, "status": "not_configured"}
    try:
        analytics = _posthog_capture(
            "feedback_submitted",
            {
                "sentiment": sentiment,
                "language": language,
                "source": "public-runtime",
                "auth_state": auth_state,
                "page": page,
                "referrer": referrer,
                "client_timezone": client_timezone,
                "client_time": client_now,
                "received_at": archive_record["received_at"],
                # Feedback text is included only when PostHog is explicitly configured.
                "feedback_text": text,
            },
        )
    except Exception:
        app.logger.exception("IMA feedback analytics provider failed")
        analytics = {"sent": False, "status": "provider_error"}

    if not stored_runtime and not analytics.get("sent"):
        return jsonify({"accepted": False, "error": "feedback could not be archived"}), 503

    return jsonify({
        "accepted": True,
        "receipt": {
            "received_at": archive_record["received_at"],
            "date_utc": archive_record["date_utc"],
            "hour_utc": archive_record["hour_utc"],
            "auth_state": auth_state,
        },
        "stored_runtime": stored_runtime,
        "analytics": analytics["status"],
        "durability": "PostHog" if analytics.get("sent") else "runtime_archive_only",
        "learning": {
            "status": "derived_and_queued",
            "applied_automatically": False,
            "reason": "Feedback is converted into a structured lesson candidate, but product changes require verification before application.",
            "lesson_tags": lesson["tags"],
        },
    }), 201

@app.get("/ima-api/growth/status")
def growth_status():
    return jsonify({
        "schema": "IMA-GLOBAL-GROWTH-1.0",
        "real_user_truth": True,
        "analytics": {
            "configured": bool(POSTHOG_API_KEY and POSTHOG_HOST),
            "provider": "PostHog" if POSTHOG_API_KEY and POSTHOG_HOST else None,
        },
        "feedback": {
            "endpoint": True,
            "runtime_archive": True,
            "daily_partitioning": True,
            "durable_provider": bool(POSTHOG_API_KEY and POSTHOG_HOST),
            "durable_provider_name": "PostHog" if POSTHOG_API_KEY and POSTHOG_HOST else None,
            "learning_queue": True,
        },
        "store_ratings": {"verified_listing": False},
        "synthetic_users": False,
        "synthetic_ratings": False,
        "note": "No user count is claimed here unless backed by verified analytics.",
    })


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
