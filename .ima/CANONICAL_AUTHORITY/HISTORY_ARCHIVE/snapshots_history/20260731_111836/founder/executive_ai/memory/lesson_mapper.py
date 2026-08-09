def map_lesson_to_signals(lesson):

    signals=[]

    text=lesson.lower()

    if "מסר" in text or "אישי" in text:
        signals.append("user_outreach")

    if "משתמש" in text or "ניסוי" in text:
        signals.append("user_testing")

    if "ערך" in text:
        signals.append("validation")

    if "לקוחות" in text:
        signals.append("customers")

    return signals
