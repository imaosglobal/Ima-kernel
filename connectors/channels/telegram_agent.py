"""Minimal Telegram transport adapter for canonical IMA.

This file is intentionally transport-only: IMA remains the single source of truth.
It does not store a second memory or implement a second assistant persona.

Activation requires operator-owned TELEGRAM_BOT_TOKEN and a canonical IMA endpoint.
"""
from __future__ import annotations

import os
from typing import Any

import requests

TELEGRAM_API = "https://api.telegram.org"


def _token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
    return token


def telegram_send_message(chat_id: str | int, text: str) -> dict[str, Any]:
    token = _token()
    response = requests.post(
        f"{TELEGRAM_API}/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def normalize_update(update: dict[str, Any]) -> dict[str, Any] | None:
    message = update.get("message") or update.get("edited_message")
    if not message or not message.get("text"):
        return None
    user = message.get("from") or {}
    chat = message.get("chat") or {}
    return {
        "channel": "telegram",
        "channel_user_id": str(user.get("id", "")),
        "channel_chat_id": str(chat.get("id", "")),
        "display_name": user.get("first_name") or user.get("username") or "",
        "message_id": str(message.get("message_id", "")),
        "text": str(message.get("text", "")),
    }


def verify_configuration() -> dict[str, Any]:
    return {
        "channel": "telegram",
        "ready_for_activation": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        "canonical_runtime": os.getenv("IMA_CHAT_URL", "").strip(),
        "shared_secret_configured": bool(os.getenv("IMA_CHANNEL_SHARED_SECRET")),
    }
