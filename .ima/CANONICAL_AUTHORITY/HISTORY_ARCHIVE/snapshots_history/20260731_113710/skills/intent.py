def detect(message):

    text=message.lower()

    if any(x in text for x in ["ללמוד","לימוד","ללמד","קורס"]):
        return "learn"

    if any(x in text for x in ["לכתוב","טקסט","שיר","פוסט"]):
        return "write"

    if any(x in text for x in ["לבנות","תוכנית","מטרה","עסק","פרויקט"]):
        return "plan"

    return "problem"
