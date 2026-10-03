import os
import secrets
import json
import subprocess
from pathlib import Path
from urllib.parse import urlencode

import requests
from flask import Blueprint, redirect, request, session, jsonify

google_auth = Blueprint("google_auth", __name__)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GMAIL_API_URL = "https://gmail.googleapis.com/gmail/v1/users/me"
GMAIL_WEB_URL = "https://mail.google.com/"
TARGET_GMAIL = "imaosglobal@gmail.com"

SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/gmail.readonly",
]

# Google identity is per signed-in user. Do not store one global user's
# token as the identity of every IMA visitor.
def _token_path_for_user(google_sub=None):
    root = Path(__file__).resolve().parents[2] / ".ima" / "gmail_bridge" / "users"
    if not google_sub:
        return root / "anonymous.json"
    safe = "".join(c for c in google_sub if c.isalnum() or c in "._-")
    return root / f"{safe}.json"

def _config():
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Google OAuth environment is not configured")
    return client_id, client_secret

def _redirect_uri():
    domain = os.environ.get("DOMAIN")
    if not domain:
        raise RuntimeError("DOMAIN is not configured")
    return domain.rstrip("/") + "/auth/google/callback"

def _save_token(token, google_sub=None):
    path = _token_path_for_user(google_sub)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(token, ensure_ascii=False), encoding="utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(path)
    os.chmod(path, 0o600)

def _load_token(google_sub=None):
    path = _token_path_for_user(google_sub)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def _refresh_if_needed(token, google_sub=None):
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        return token

    import time
    expires_at = token.get("expires_at", 0)
    if expires_at and time.time() < expires_at - 60:
        return token

    client_id, client_secret = _config()
    response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=20,
    )
    response.raise_for_status()
    refreshed = response.json()
    refreshed["refresh_token"] = refresh_token
    refreshed["expires_at"] = time.time() + int(refreshed.get("expires_in", 3600))
    _save_token(refreshed, google_sub)
    return refreshed

@google_auth.get("/auth/google")
def google_login():
    client_id, _ = _config()
    state = secrets.token_urlsafe(32)
    session["google_oauth_state"] = state
    params = {
        "client_id": client_id,
        "redirect_uri": _redirect_uri(),
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": state,
        "access_type": "offline",
        "prompt": "select_account",
    }
    # Deliberately no login_hint: every visitor must be able to choose
    # their own Google account.
    return redirect(GOOGLE_AUTH_URL + "?" + urlencode(params))

@google_auth.get("/auth/google/open")
def open_gmail():
    url = GMAIL_WEB_URL
    try:
        subprocess.Popen(["termux-open-url", url])
        method = "termux-open-url"
    except Exception:
        import webbrowser
        webbrowser.open(url)
        method = "webbrowser"
    return jsonify({"ok": True, "opened": True, "url": url, "method": method})

@google_auth.get("/auth/google/callback")
def google_callback():
    expected_state = session.pop("google_oauth_state", None)
    received_state = request.args.get("state")
    if not expected_state or not received_state:
        return jsonify({"error": "OAuth state missing"}), 400
    if not secrets.compare_digest(expected_state, received_state):
        return jsonify({"error": "OAuth state mismatch"}), 400

    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Google authorization failed", "details": request.args.get("error")}), 400

    client_id, client_secret = _config()
    redirect_uri = _redirect_uri()
    token_response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=20,
    )
    token_response.raise_for_status()
    token = token_response.json()
    if not token.get("access_token"):
        return jsonify({"error": "Google did not return access token"}), 502

    import time
    token["expires_at"] = time.time() + int(token.get("expires_in", 3600))

    access_token = token["access_token"]
    user_response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": "Bearer " + access_token},
        timeout=20,
    )
    user_response.raise_for_status()
    profile = user_response.json()
    google_sub = profile.get("sub")
    email = profile.get("email")
    if not google_sub or not email:
        return jsonify({"error": "Incomplete Google identity"}), 502

    _save_token(token, google_sub)

    session["user_id"] = "google:" + google_sub
    session["google_sub"] = google_sub
    session["user_email"] = email
    session["user_name"] = profile.get("name", "")
    session["gmail_connected"] = True

    frontend = os.environ.get("FRONTEND_URL")
    if frontend:
        return redirect(frontend.rstrip("/") + "/")
    return jsonify({
        "ok": True,
        "google_connected": True,
        "gmail_connected": True,
        "email": email,
    })

@google_auth.get("/auth/google/gmail/status")
def gmail_status():
    google_sub = session.get("google_sub")
    if not google_sub:
        return jsonify({"connected": False, "authenticated": False}), 401
    token = _load_token(google_sub)
    if not token:
        return jsonify({"connected": False})
    try:
        token = _refresh_if_needed(token, google_sub)
        response = requests.get(
            GMAIL_API_URL + "/labels/INBOX",
            headers={"Authorization": "Bearer " + token["access_token"]},
            timeout=20,
        )
        return jsonify({"connected": response.ok, "gmail": response.ok, "status_code": response.status_code})
    except Exception as e:
        return jsonify({"connected": False, "error": str(e)}), 502

@google_auth.get("/auth/google/gmail/messages")
def gmail_messages():
    google_sub = session.get("google_sub")
    if not google_sub:
        return jsonify({"connected": False, "error": "AUTH_REQUIRED"}), 401
    token = _load_token(google_sub)
    if not token:
        return jsonify({"connected": False, "error": "GMAIL_NOT_CONNECTED"}), 401
    try:
        token = _refresh_if_needed(token, google_sub)
        params = {
            "maxResults": min(int(request.args.get("maxResults", 10)), 50),
            "q": request.args.get("q", "from:(notifications@github.com) newer_than:7d (failed OR failure)")
        }
        response = requests.get(
            GMAIL_API_URL + "/messages",
            headers={"Authorization": "Bearer " + token["access_token"]},
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"connected": False, "error": str(e)}), 502

@google_auth.get("/me")
def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"authenticated": False}), 401
    return jsonify({
        "authenticated": True,
        "user_id": user_id,
        "email": session.get("user_email"),
        "name": session.get("user_name"),
        "gmail_connected": bool(session.get("gmail_connected")),
    })

@google_auth.post("/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})
