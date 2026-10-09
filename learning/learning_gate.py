"""Consent-aware gate for learning from incoming events.

Personal conversation storage and shared/self-learning are separate operations.
User-originated content is not eligible for learning unless the caller explicitly
records authorization. Missing consent is a deny, not an inferred yes.
"""

def should_learn(event):
    if not isinstance(event, dict):
        return False

    source = event.get("source", "user")
    text = str(event.get("text", ""))

    # Private user contributions must never become learning material by default.
    # Callers must provide an explicit, auditable authorization decision.
    if source == "user" and event.get("learning_authorized") is not True:
        return False

    if event.get("privacy_class") == "private":
        return False

    if event.get("consent_revoked") is True:
        return False

    ignore = [
        "תוכנית שיפור מערכת",
        "העמקת יכולת IMA",
        "דפוסים חוזרים",
        "מהזיכרון ומההיסטוריה",
    ]
    if any(marker in text for marker in ignore):
        return False

    return len(text.strip()) >= 8
