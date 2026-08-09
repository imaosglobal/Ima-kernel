from pathlib import Path
import shutil
import time

path = Path("ima_system.py")

if not path.exists():
    raise SystemExit("ima_system.py not found")

backup = Path(f"ima_system_before_routing_fix_{int(time.time())}.py")
shutil.copy(path, backup)

text = path.read_text(encoding="utf-8")

# Fix emotion priority in router
old = '''    if intent == "information_request":
        return "information"

    emotion = ima_emotion_layer(question, [])

    if emotion:
        return "emotion"

    return "conversation"
'''

new = '''    if intent == "information_request":
        return "information"

    emotion = ima_emotion_layer(question, [])

    if emotion:
        return "emotion"

    return "conversation"
'''

# This section already exists, so no replacement needed.
# Add capability/learning handlers before final fallback.
marker = '''    return {
        "text": "אני IMA. אני כאן כדי להקשיב, להבין ולעזור לך דרך השיחה שלנו.",
        "confidence": 0.7
    }
'''

insert = '''    if any(x in question for x in [
        "למדת",
        "מה למדת",
        "מה חדש אצלך",
        "האם השתנית"
    ]):
        return {
            "text": "אני IMA. אני לומדת דרך אירועים, זיכרון וקשרים שנשמרים במערכת.",
            "confidence": 0.85
        }

    if "יכולות" in question or "מחובר" in question:
        return {
            "text": "אני IMA. מחוברות כרגע שכבות זיכרון, ידע, שפה, למידה ורפלקציה.",
            "confidence": 0.85
        }

''' + marker

if "מחוברות כרגע שכבות זיכרון" not in text:
    text = text.replace(marker, insert)

path.write_text(text, encoding="utf-8")

print("BACKUP:", backup)
print("PATCH COMPLETE")
