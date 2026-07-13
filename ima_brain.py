import json, os
from learning.learning_memory import store_pattern
from learning.historical_inference import get_conclusions

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



def extract_patterns(events):
    text=" ".join(
        [
            e.get("data",{}).get("text","")
            for e in events[-500:]
            if e.get("type")=="QUESTION"
        ]
    ).lower()

    patterns=[]

    groups={
        "טכנולוגיה ומערכות": [
            "ima","בינה","קוד","מערכת","קרנל",
            "תכנות","ai","רשת","מנוע"
        ],
        "פילוסופיה ותודעה": [
            "אמת","תודעה","משמעות","אני","חיים"
        ],
        "יצירה והתפתחות": [
            "שיר","יצירה","ללמוד","שיפור","התפתחות"
        ],
        "אדם וריפוי": [
            "כאב","ריפוי","רגש","נפש"
        ]
    }

    for name,words in groups.items():
        found=sum(1 for w in words if w in text)
        if found:
            patterns.append(name)

    if not patterns:
        patterns.append("עדיין אין מספיק מידע לזיהוי דפוסים")

    return patterns

def answer(question, events):

    q = question.lower()

    if "מטרה" in q or "חזון" in q:
        return (
            "המטרה של IMA היא לבנות מערכת הלומדת, "
            "זוכרת ומתפתחת תוך שמירה על משמעות ואחריות.\n\n"
            "טכנולוגיה צריכה להעצים את האדם ולא להחליף את האנושי."
        )

    if "למדת ממני" in q or "לומדת ממני" in q:
        patterns = extract_patterns(events)

        for pattern in patterns:
            store_pattern(pattern)

        history = get_conclusions()

        return (
            "מהזיכרון ומההיסטוריה אני מזהה:\n\n"
            + "\n".join("- " + c for c in history.get("conclusions",[]))
            + "\n\nדפוסים חוזרים:\n"
            + "\n".join("- " + p for p in patterns)
        )

    if "שפר" in q:
        return (
            "נקודות לשיפור:\n"
            "1. הפרדת זיכרון מחשיבה.\n"
            "2. חיבור ידע פנימי ל-Brain.\n"
            "3. הפקת מסקנות מהיסטוריית האירועים."
        )

    if "תודעה" in q:
        return "תודעה היא תהליך של חוויה, זיכרון ופרשנות פנימית של קיום."

    if "כאב" in q:
        return "כאב הוא אות של מערכת העצבים שמבקש תשומת לב ולא בהכרח סכנה."

    return ""
