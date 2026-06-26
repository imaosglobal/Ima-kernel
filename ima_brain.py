import json, os

LEDGER = ".ima/ledger.jsonl"


# -------------------------
# MEMORY
# -------------------------
def load_events():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(l) for l in f if l.strip()]


def recent_context(events, limit=20):
    return events[-limit:]


# -------------------------
# (STUB) WEB LAYER
# -------------------------
def web_search(query):
    return [
        f"לא נמצא חיפוש אמיתי עבור: {query}",
        "יש לחבר API חיצוני (google/bing/rag) כדי להרחיב"
    ]


# -------------------------
# CORE "MOTHER" RESPONSE ENGINE
# -------------------------
def answer(question, events):
    context = recent_context(events)

    memory_hits = [
        e["data"] for e in context if e["type"] == "QUESTION"
    ]

    # basic synthesis (placeholder intelligence layer)
    if "תודעה" in question:
        return "תודעה היא תהליך של חוויה, זיכרון ופרשנות פנימית של קיום."

    if "כאב" in question:
        return "כאב הוא אות של מערכת העצבים שמבקש תשומת לב ולא בהכרח סכנה."

    if memory_hits:
        return f"אני זוכרת ששאלת דברים דומים. השאלה שלך היא: {question}"

    # fallback
    web = web_search(question)
    return " | ".join(web)
