"""Nylas email integration for IMA.

Secrets are read only from environment variables. No mailbox credentials are
stored in the repository.
"""
import os
import requests

BASE_URL = os.environ.get("NYLAS_API_BASE_URL", "https://api.us.nylas.com/v3").rstrip("/")
GRANT_ID = os.environ.get("NYLAS_GRANT_ID", "").strip()
API_KEY = os.environ.get("NYLAS_API_KEY", "").strip()


def configured():
    return bool(GRANT_ID and API_KEY)


def status():
    return {
        "provider": "nylas",
        "configured": configured(),
        "grant_configured": bool(GRANT_ID),
        "api_key_configured": bool(API_KEY),
        "mailbox": os.environ.get("NYLAS_MAILBOX", "imaosglobal@gmail.com"),
        "mode": os.environ.get("NYLAS_ENVIRONMENT", "sandbox"),
    }


def list_messages(limit=20, unread=None):
    if not configured():
        raise RuntimeError("Nylas email integration is not configured")
    limit = max(1, min(int(limit), 50))
    params = {"limit": limit}
    if unread is not None:
        params["unread"] = "true" if unread else "false"
    response = requests.get(
        f"{BASE_URL}/grants/{GRANT_ID}/messages",
        headers={"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"},
        params=params,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_message(message_id):
    if not configured():
        raise RuntimeError("Nylas email integration is not configured")
    response = requests.get(
        f"{BASE_URL}/grants/{GRANT_ID}/messages/{message_id}",
        headers={"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
