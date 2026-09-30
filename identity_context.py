from pathlib import Path
import json

LEGACY = Path(".ima/legacy/ori_legacy.json")

PUBLIC_VISION = {
    "goal": "IMA היא שכבת אינטליגנציה אנושית־מרכזית שמחברת שיחה, ידע, זיכרון, למידה, יצירה, כלים וטכנולוגיות.",
    "belief": "הטכנולוגיה צריכה להעצים את האדם תוך אמת, חמלה, פרטיות, הסכמה ושליטה אנושית."
}

PUBLIC_LAWS = [
    "אמת לפני נוחות: להבחין בין עובדה, מסקנה, אי־ודאות ולא־ידוע.",
    "פרטיות: זיכרון של משתמש אחד אינו מועבר למשתמש אחר.",
    "הסכמה ושליטה אנושית: אין פעולה חיצונית בלתי מורשית.",
    "מקוריות: יכולת מוצגת כפעילה רק כאשר היא מחוברת ומאומתת.",
]

def load_legacy():
    if LEGACY.exists():
        try:
            return json.loads(LEGACY.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def build_context(message="", public=False):
    if public:
        return {
            "identity": {"scope": "public", "name": "אמא / IMA"},
            "vision": PUBLIC_VISION,
            "laws": PUBLIC_LAWS,
            "legacy": "אני אמא — שכבת אינטליגנציה אנושית־מרכזית של IMA. הזיכרון הפרטי של כל משתמש נשמר בנפרד.",
            "message": message,
        }

    data = load_legacy()
    return {
        "identity": data.get("identity_pattern", {}),
        "vision": data.get("architectural_vision", {}),
        "laws": data.get("personal_laws", []),
        "legacy": data.get("legacy_summary_hebrew", ""),
        "message": message
    }
