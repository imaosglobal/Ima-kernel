from __future__ import annotations

from typing import Any

from learning.sources.facebook_browser import fetch

FACEBOOK_URL = "https://www.facebook.com/share/1FFdWxZt2a/"
CREATOR_ID = "creator_001"


def search(question: str) -> dict[str, Any]:
    result = fetch(question, FACEBOOK_URL)

    result.update({
        "registry_source": "Ori Cohen — Facebook Creator Source",
        "learning_enabled": True,
        "continuous_scan": True,
        "canonical_source": True,
        "read_only": True,
        "content_types": [
            "poetry",
            "songs",
            "lyrics",
            "posts",
            "ideas",
            "creative_writing",
            "media",
        ],
    })

    return result
