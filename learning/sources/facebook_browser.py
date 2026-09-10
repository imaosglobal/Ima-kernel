from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path

FACEBOOK_URL = "https://www.facebook.com/share/1FFdWxZt2a/"
CREATOR_ID = "creator_001"


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()


def fetch_via_http(url: str = FACEBOOK_URL):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 16) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140 Mobile Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": "he-IL,he;q=0.9,en;q=0.8",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            raw = response.read()
            return {
                "ok": True,
                "method": "http",
                "status": response.status,
                "url": response.url,
                "html": raw.decode("utf-8", errors="ignore"),
            }
    except Exception as exc:
        return {
            "ok": False,
            "method": "http",
            "error": type(exc).__name__,
            "message": str(exc),
        }


def open_android_browser(url: str = FACEBOOK_URL):
    """
    Opens the user's real Android browser.

    This does not bypass Facebook authentication.
    If Facebook requires login, the user must already be
    authenticated in the browser.
    """
    try:
        subprocess.Popen(
            ["termux-open-url", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return {
            "ok": True,
            "method": "android_browser",
            "url": url,
        }
    except Exception as exc:
        return {
            "ok": False,
            "method": "android_browser",
            "error": type(exc).__name__,
            "message": str(exc),
        }


def fetch(question: str = "", url: str = FACEBOOK_URL):
    result = fetch_via_http(url)

    if result.get("ok"):
        html = result.get("html", "")
        return {
            "source": "Ori Cohen — Facebook Creator Source",
            "creator_id": CREATOR_ID,
            "creator": "Ori Cohen",
            "source_url": url,
            "type": "creator_content_source",
            "content": _clean(html),
            "confidence": 0.95,
            "retrieved_at": time.time(),
            "method": "http",
        }

    browser = {"ok": False, "method": "disabled_automatic_browser"}

    return {
        "source": "Ori Cohen — Facebook Creator Source",
        "creator_id": CREATOR_ID,
        "creator": "Ori Cohen",
        "source_url": url,
        "type": "creator_content_source",
        "content": "",
        "content_available": False,
        "requires_browser_session": True,
        "browser_opened": browser.get("ok", False),
        "http_error": result,
        "confidence": 0.0,
        "retrieved_at": time.time(),
        "method": "android_browser",
    }
