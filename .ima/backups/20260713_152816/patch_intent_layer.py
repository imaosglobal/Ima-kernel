from pathlib import Path

p = Path("ima_system.py")
s = p.read_text()

if "def detect_intent" not in s:

    s += r'''

# -------------------------
# IMA INTENT LAYER
# -------------------------

def detect_intent(question):

    technical_words = [
        "איך עובד",
        "הסבר",
        "קוד",
        "תכנות",
        "מנוע",
        "מערכת",
        "טכני",
        "למה זה קורה"
    ]

    info_words = [
        "מזג האוויר",
        "חדשות",
        "מחיר",
        "שעה",
        "מיקום"
    ]

    if any(x in question for x in technical_words):
        return "technical_request"

    if any(x in question for x in info_words):
        return "information_request"

    return "conversation"
'''

    p.write_text(s)
    print("intent layer added")
else:
    print("exists")
