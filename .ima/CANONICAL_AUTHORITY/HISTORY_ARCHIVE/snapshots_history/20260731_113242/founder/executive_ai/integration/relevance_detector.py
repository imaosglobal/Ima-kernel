KEYWORDS = [
    "לקוח",
    "משתמש",
    "השקעה",
    "משקיע",
    "מוצר",
    "שוק",
    "מתחר",
    "החלטה",
    "אסטרטגיה",
    "צוות",
    "פאונדר",
    "חברה"
]


def is_founder_relevant(message):

    text = str(message).lower()

    matches = [
        k for k in KEYWORDS
        if k in text
    ]

    return {
        "relevant": len(matches) > 0,
        "signals": matches
    }
