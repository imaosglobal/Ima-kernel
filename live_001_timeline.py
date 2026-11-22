"""LIVE-001 per-user timeline: the auditable history of an interactive intelligence window.

The timeline records what the user/device window did, what was observed, and whether the
result was verified. Secrets and high-risk raw inputs are deliberately redacted.
"""

import hashlib
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit

import requests

_TABLE = "ima_live_timeline"
_SECRET_KEYS = {
    "password", "passwd", "token", "access_token", "refresh_token", "authorization",
    "cookie", "device_key", "secret", "api_key", "apikey", "credential", "code",
}


def _safe_url(value):
    try:
        parts = urlsplit(str(value))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    except Exception:
        return ""


def _safe_value(key, value):
    key_l = str(key).lower()
    if key_l in _SECRET_KEYS or any(x in key_l for x in _SECRET_KEYS):
        return {"redacted": True}
    if key_l in {"text", "value", "content", "input", "query"}:
        raw = str(value or "")
        return {"redacted": True, "length": len(raw), "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()}
    if key_l in {"url", "href", "target_url"}:
        return _safe_url(value)
    if isinstance(value, dict):
        return {str(k): _safe_value(k, v) for k, v in value.items() if str(k).lower() not in _SECRET_KEYS}
    if isinstance(value, list):
        return [_safe_value("", v) for v in value[:50]]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)[:500]


def sanitize(value):
    return _safe_value("", value)


def _headers():
    key = os.environ.get("SUPABASE_SERVICE_KEY", "").strip()
    if not key:
        raise RuntimeError("SUPABASE_SERVICE_KEY is not configured")
    return {
        "apikey": key,
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _base():
    base = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    if not base:
        raise RuntimeError("SUPABASE_URL is not configured")
    return base


def record_event(
    *,
    user_id,
    session_id=None,
    event_type,
    phase="observe",
    status="recorded",
    action=None,
    device_id=None,
    command_id=None,
    payload=None,
    result=None,
    provenance=None,
    verified_at=None,
):
    """Append one immutable timeline event. Failure is non-blocking for LIVE-001."""
    if not user_id:
        return {"recorded": False, "status": "missing_user"}
    occurred_at = datetime.now(timezone.utc).isoformat()
    row = {
        "user_id": str(user_id),
        "session_id": str(session_id) if session_id else None,
        "device_id": device_id,
        "command_id": command_id,
        "event_type": str(event_type)[:120],
        "action": str(action)[:120] if action else None,
        "phase": str(phase)[:40],
        "status": str(status)[:40],
        "payload": sanitize(payload or {}),
        "result": sanitize(result or {}),
        "provenance": sanitize(provenance or {
            "system": "LIVE-001",
            "contract": "observe-understand-decide-authorize-act-verify-learn-improve",
        }),
        "occurred_at": occurred_at,
        "verified_at": verified_at,
    }
    try:
        response = requests.post(
            _base() + "/rest/v1/" + _TABLE,
            headers=_headers(),
            json=row,
            timeout=8,
        )
        if response.status_code not in (200, 201):
            return {"recorded": False, "status": "archive_error", "http_status": response.status_code}
        data = response.json() if response.content else []
        item = data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else {})
        return {"recorded": bool(item.get("id")), "status": "recorded" if item.get("id") else "unverified", "id": item.get("id"), "occurred_at": occurred_at}
    except Exception as exc:
        return {"recorded": False, "status": "archive_unavailable", "error": str(exc)[:240]}


def session_id_from_request(request):
    return (
        request.headers.get("X-IMA-Live-Session", "").strip()
        or (request.get_json(silent=True) or {}).get("live_session_id")
        or None
    )
