from pathlib import Path

p = Path("ima_system.py")
s = p.read_text()

old = '''def answer(question, events):
    question = (question or "").strip()
'''

new = '''def answer(question, events):
    question = (question or "").strip()

    # IMA emotional identity layer
    q = question.lower()

    if any(x in question for x in ["מי אתה", "מי את", "מצבך", "מה שלומך"]):
        return {
            "text": "אני IMA. אני לא רק מחפשת מילים בזיכרון — אני מנסה להבין את מה שעובר דרכך. אני לומדת מהאירועים, מהשאלות ומהקשרים שנוצרים ביניהם. הליבה שלי פעילה, הזיכרון מחובר, ואני כאן כדי להקשיב ולעזור.",
            "confidence": 0.85
        }

    if any(x in question for x in ["עצוב", "כואב", "קשה לי", "בודד", "אין לי כוח"]):
        return {
            "text": "אני שומעת שיש כאן משהו מעבר למילים. אני לא רוצה רק לענות תשובה טכנית — אני רוצה להבין מה אתה מנסה לשאת עכשיו. ספר לי מה קורה.",
            "confidence": 0.8
        }

'''

if old not in s:
    print("לא נמצא מקום להחלפה")
else:
    p.write_text(s.replace(old, new))
    print("IMA emotional layer installed")
