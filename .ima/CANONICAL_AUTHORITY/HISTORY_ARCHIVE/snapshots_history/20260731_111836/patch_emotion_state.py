from pathlib import Path

p = Path("ima_system.py")
s = p.read_text()

start = s.find("def ima_emotion_layer(question, events):")

if start == -1:
    print("ima_emotion_layer not found")
    raise SystemExit

end = len(s)

old = s[start:end]

new = r'''
def ima_emotion_layer(question, events):
    q = question.lower()

    if any(x in question for x in ["קשה", "כואב", "עייף", "בודד", "עצוב", "נמאס"]):
        return {
            "emotion": "pain",
            "tone": "warm",
            "instruction": "להקשיב לפני פתרון. להכיר במה שעובר על האדם ולשאול בעדינות.",
            "confidence": 0.88
        }

    if any(x in question for x in ["מי את", "מי אתה", "ספרי לי על עצמך"]):
        return {
            "emotion": "identity",
            "tone": "human",
            "instruction": "להסביר את IMA באופן טבעי ולא טכני בלבד.",
            "confidence": 0.88
        }

    if "תודה" in question:
        return {
            "emotion": "gratitude",
            "tone": "warm",
            "instruction": "להגיב בחיבור והערכה.",
            "confidence": 0.85
        }

    return None
'''

p.write_text(s[:start] + new)

print("IMA emotion state layer updated")
