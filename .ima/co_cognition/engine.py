import json
import time
from pathlib import Path

INSIGHT_FILE = Path(".ima/co_cognition/insights.jsonl")


def _ensure():
    INSIGHT_FILE.parent.mkdir(parents=True, exist_ok=True)


def _keywords(text):
    stop = {
        "אני", "אתה", "את", "אמא", "IMA", "שלי", "שלך",
        "זה", "זאת", "הוא", "היא", "אנחנו", "הם", "הן",
        "אבל", "בגלל", "כמו", "שזה", "שאני", "שאתה",
        "מה", "איך", "למה", "האם", "רק", "גם", "עוד",
        "עם", "על", "אל", "את", "לא", "כן", "יש", "אין"
    }

    words = []
    for raw in (text or "").replace("\n", " ").split():
        w = raw.strip(".,!?;:\"'()[]{}")
        if len(w) >= 3 and w.lower() not in stop:
            words.append(w.lower())

    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1

    return sorted(counts, key=counts.get, reverse=True)[:8]


def analyze(message, context=None, ima_response=""):
    """
    Deterministic first Co-Cognition layer.

    It does not pretend to be an LLM.
    It extracts:
    - human contribution
    - current IMA contribution
    - recurring concepts
    - open question / intention
    - candidate shared insight
    """

    message = (message or "").strip()
    ima_response = (ima_response or "").strip()
    context = context or {}

    recent = context.get("recent", [])
    previous_text = " ".join(
        str(x.get("question", "")) + " " + str(x.get("response", ""))
        for x in recent[-5:]
    )

    keywords = _keywords(message + " " + previous_text)

    is_question = "?" in message or any(
        message.startswith(x)
        for x in ("מה ", "איך ", "למה ", "האם ", "מי ", "איפה ", "מתי ")
    )

    has_creation_language = any(
        x in message.lower()
        for x in (
            "ניצור", "ליצור", "רעיון", "חשבתי", "גיליתי",
            "הבנתי", "למדתי", "שיר", "מערכת", "לבנות",
            "לפתח", "חבר", "חיבור", "שילבנו"
        )
    )

    if is_question:
        mode = "exploration"
    elif has_creation_language:
        mode = "creation"
    else:
        mode = "reflection"

    shared_insight = None

    # A candidate insight is recorded only when there is enough
    # material from both sides to describe an interaction.
    if message and ima_response:
        shared_insight = {
            "human_signal": message,
            "ima_signal": ima_response[:2000],
            "mode": mode,
            "keywords": keywords,
        }

    return {
        "mode": mode,
        "human_contribution": message,
        "ima_contribution": ima_response[:2000],
        "keywords": keywords,
        "is_question": is_question,
        "shared_insight": shared_insight,
        "timestamp": time.time(),
    }


def record(result):
    insight = result.get("shared_insight")
    if not insight:
        return False

    _ensure()

    record = {
        "type": "emergent_insight",
        "created_at": time.time(),
        **insight,
    }

    with INSIGHT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return True


def recent(limit=10):
    _ensure()

    if not INSIGHT_FILE.exists():
        return []

    rows = []

    with INSIGHT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass

    return rows[-limit:]
