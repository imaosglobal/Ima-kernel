from __future__ import annotations

from pathlib import Path
import json
import urllib.parse
import urllib.request


LOCAL_ROOTS = [
    Path("learning"),
    Path("founder"),
    Path("product"),
]


def _normalize(question: str) -> str:
    return (
        question
        .replace("מה זה ", "")
        .replace("מהי ", "")
        .replace("?", "")
        .strip()
        .lower()
    )


def local_search(question: str):
    term = _normalize(question)

    if not term:
        return None

    for root in LOCAL_ROOTS:
        if not root.exists():
            continue

        for path in root.rglob("*.json"):
            if "__pycache__" in path.parts:
                continue
            if "_backup" in path.name:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue

            if term in text.lower():
                return {
                    "content": text[:5000],
                    "source": "IMA Local Knowledge",
                    "url": str(path),
                    "confidence": 0.9,
                }

    return None


def wikipedia_search(question: str):
    try:
        term = _normalize(question)

        url = (
            "https://he.wikipedia.org/w/api.php?"
            "action=query&list=search&"
            "srsearch="
            + urllib.parse.quote(term)
            + "&format=json"
        )

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "IMA-Knowledge-Agent/1.0"},
        )

        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        results = data.get("query", {}).get("search", [])

        if results:
            item = results[0]
            title = item.get("title", "")

            return {
                "content": item.get("snippet", ""),
                "source": "Wikipedia",
                "url": (
                    "https://he.wikipedia.org/wiki/"
                    + urllib.parse.quote(
                        title.replace(" ", "_")
                    )
                ),
                "confidence": 0.8,
            }

    except Exception:
        pass

    return None


def get_real_source(question: str):
    local = local_search(question)

    if local:
        return local

    return wikipedia_search(question)
