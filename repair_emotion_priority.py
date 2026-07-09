from pathlib import Path
import shutil
import time

path = Path("ima_system.py")

backup = f"ima_system_before_emotion_priority_{int(time.time())}.py"
shutil.copy(path, backup)

text = path.read_text(encoding="utf-8")

old = '''def ima_router(question):

    intent = detect_intent(question)

    if any(x in question for x in [
        "מי את",
        "מי אתה",
        "מה את",
        "מה מצבך"
    ]):
        return "identity"

    if intent == "technical_request":
        return "technical"

    if intent == "information_request":
        return "information"

    emotion = ima_emotion_layer(question, [])

    if emotion:
        return "emotion"

    return "conversation"
'''

new = '''def ima_router(question):

    if any(x in question for x in [
        "מי את",
        "מי אתה",
        "מה את",
        "מה מצבך"
    ]):
        return "identity"

    # Emotion has priority over information keywords
    emotion = ima_emotion_layer(question, [])

    if emotion:
        return "emotion"

    intent = detect_intent(question)

    if intent == "technical_request":
        return "technical"

    if intent == "information_request":
        return "information"

    return "conversation"
'''

if old not in text:
    print("ROUTER BLOCK NOT FOUND")
else:
    text = text.replace(old,new)
    path.write_text(text,encoding="utf-8")
    print("BACKUP:", backup)
    print("EMOTION PRIORITY FIX COMPLETE")
