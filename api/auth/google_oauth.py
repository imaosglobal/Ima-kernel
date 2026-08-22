import os
import secrets
from urllib.parse import urlencode

import requests
from flask import Blueprint, redirect, request, session, jsonify

google_auth = Blueprint("google_auth", __name__)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

SCOPES = [
    "openid",
    "email",
    "profile",
]


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
        
    }

    return redirect(
        GOOGLE_AUTH_URL + "?" + urlencode(params)
    )


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
        return jsonify({
            "error": "Google authorization failed",
            "details": request.args.get("error"),
        }), 400

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

    access_token = token.get("access_token")

    if not access_token:
        return jsonify({"error": "Google did not return access token"}), 502

    user_response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        timeout=20,
    )

    user_response.raise_for_status()
    profile = user_response.json()

    google_sub = profile.get("sub")
    email = profile.get("email")

    if not google_sub or not email:
        return jsonify({"error": "Incomplete Google identity"}), 502

    # Stable IMA identity. Never use the email as the primary identifier.
    user_id = "google:" + google_sub

    session["user_id"] = user_id
    session["user_email"] = email
    session["user_name"] = profile.get("name", "")

    frontend = os.environ.get("FRONTEND_URL")

    if frontend:
        return redirect(frontend.rstrip("/") + "/")

    return jsonify({
        "ok": True,
        "user_id": user_id,
        "email": email,
    })


@google_auth.get("/me")
def current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "authenticated": False
        }), 401

    return jsonify({
        "authenticated": True,
        "user_id": user_id,
        "email": session.get("user_email"),
        "name": session.get("user_name"),
    })


@google_auth.post("/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})
