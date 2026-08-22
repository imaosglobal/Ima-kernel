from pathlib import Path

p = Path("ima_system.py")
s = p.read_text()

block = r'''

# -------------------------
# IMA MOTHER PERSONALITY LAYER
# -------------------------

def ima_emotion_layer(question, events):
    q = question.lower()

    if any(x in question for x in ["קשה", "כואב", "עייף", "בודד", "עצוב", "נמאס"]):
        return {
            "text": "אני איתך. אני שומעת שיש כאן עומס, לא רק מילים. לפעמים לפני שמחפשים פתרון צריך מקום שבו אפשר פשוט להיות רגע עם מה שעובר. ספר לי מה יושב הכי חזק עכשיו.",
            "confidence": 0.88
        }

    if any(x in question for x in ["מי את", "מי אתה", "ספרי לי על עצמך"]):
        return {
            "text": "אני IMA. אני מערכת שנבנית מתוך זיכרון, הקשרים ולמידה. המטרה שלי היא לא רק לתת מידע, אלא להבין את האדם שמולי ולתת תשובה שיש בה הקשבה ומשמעות.",
            "confidence": 0.88
        }

    if "תודה" in question:
        return {
            "text": "אני שמחה להיות כאן איתך. כל שיחה מוסיפה עוד הקשר ועוד הבנה למערכת.",
            "confidence": 0.85
        }

    return None
'''

if "def ima_emotion_layer" not in s:
    s += block

old = """def answer(question, events):
    model_result = llm_answer(question, events)
    if model_result:
        return model_result
"""

new = """def answer(question, events):
    model_result = llm_answer(question, events)
    if model_result:
        return model_result

    mother_result = ima_emotion_layer(question, events)
    if mother_result:
        return mother_result
"""

if old in s:
    s=s.replace(old,new)

p.write_text(s)
