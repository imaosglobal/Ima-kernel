import subprocess
import json, time, os, subprocess

LEDGER = ".ima/ledger.jsonl"


# -------------------------
# MEMORY
# -------------------------
def load_events():
    if not os.path.exists(LEDGER):
        return []
    try:
        return [json.loads(l) for l in open(LEDGER) if l.strip()]
    except:
        return []


def emit(event_type, **data):
    os.makedirs(".ima", exist_ok=True)
    event = {"ts": time.time(), "type": event_type, "data": data}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\n")


# -------------------------
# SIMPLE MEMORY QUERY
# -------------------------
def memory_summary(events):
    questions = [e for e in events if e["type"] == "QUESTION"]
    answers = [e for e in events if e["type"] == "ANSWER"]
    return {
        "questions": len(questions),
        "answers": len(answers)
    }


# -------------------------
# ANSWER ENGINE (SAFE + NEVER NONE)
# -------------------------
def answer(question, events):

    personality = load_personality()

    model_result = llm_answer(question, events)
    if model_result:
        return model_result

    mother_state = ima_emotion_layer(question, events)
    if mother_state:
        generated = mother_generate(
            question,
            mother_state.get("emotion"),
            events
        )
        if generated:
            return generated

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


    if not question:
        return {"text": "שאלה ריקה", "confidence": 0.0}

    q_lower = question.lower()

    # domain rules (minimal brain)
    if "תודעה" in question:
        text = "תודעה היא חוויה פנימית של קיום, זיכרון ופרשנות של העולם."
        return {"text": text, "confidence": 0.9}

    if "כאב" in question:
        text = "כאב הוא אות עצבי שמתריע על שינוי או עומס במערכת הגוף."
        return {"text": text, "confidence": 0.85}

    if any(x in question for x in ["אני", "מי אתה", "מי את", "מה מצבך", "מצב המערכת"]):
        text = "אני IMA — מערכת מבוססת אירועים, זיכרון ולמידה. מצב הליבה תקין, הזיכרון פעיל, ומנוע האירועים מוכן."
        return {"text": text, "confidence": 0.85}

    # fallback memory-based response
    mem = memory_summary(events)

    return {
        "text": f"אני עדיין לומדת. יש לי {mem['questions']} שאלות ו-{mem['answers']} תשובות במערכת.",
        "confidence": 0.4
    }


# -------------------------
# PIPELINE (NO None EVER)
# -------------------------
def ask(question, qid=None):
    if qid is None:
        qid = str(int(time.time() * 1000))

    emit("QUESTION", id=qid, text=question)

    events = load_events()
    result = answer(question, events) or {}

    text = result.get("text", "אין תשובה זמינה")
    conf = result.get("confidence", 0.0)

    emit("ANSWER", id=qid, text=text, confidence=conf)

    return {"id": qid, "text": text, "confidence": conf}


# -------------------------
# GIT SNAPSHOT (SAFE ONCE)
# -------------------------
def git_snapshot():
    subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL)

    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return

    subprocess.run(["git", "commit", "-m", f"auto {int(time.time())}"])


# -------------------------
# STATUS
# -------------------------
def status():
    events = load_events()
    mem = memory_summary(events)

    print("=== IMA CLEAN v2 ===")
    print("EVENTS:", len(events))
    print("QUESTIONS:", mem["questions"])
    print("ANSWERS:", mem["answers"])


# -------------------------
# CLI
# -------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "ask":
        print(ask(" ".join(sys.argv[2:])))
    else:
        status()


def boot_event():
    emit("KERNEL_BOOT")


def ready_event():
    emit("KERNEL_READY")



# -------------------------
# LLM CONNECTOR
# -------------------------
def llm_answer(question, events):
    """
    Placeholder for real language model.
    Priority:
    1. OpenAI API
    2. Local model
    3. Emotional fallback
    """
    import os

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role":"system",
                        "content":
                        "את IMA. את אמא טכנולוגית. "
                        "עני בעברית טבעית, אנושית, חמה ועמוקה. "
                        "אל תישמעי כמו תוכנה."
                    },
                    {
                        "role":"user",
                        "content":question
                    }
                ]
            )

            return {
                "text": response.choices[0].message.content,
                "confidence": 0.95
            }

        except Exception as e:
            pass

    return None


# -------------------------
# IMA MOTHER PERSONALITY LAYER
# -------------------------



def ima_emotion_layer(question, events):
    q = question.lower()

    if any(x in question for x in ["קשה", "כואב", "עייף", "בודד", "עצוב", "נמאס"]):
        return {
            "emotion": "pain",
            "confidence": 0.88
        }

    if any(x in question for x in ["מי את", "מי אתה", "ספרי לי על עצמך"]):
        return {
            "emotion": "identity",
            "confidence": 0.88
        }

    if "תודה" in question:
        return {
            "emotion": "gratitude",
            "confidence": 0.85
        }

    return None


# -------------------------
# IMA PERSONALITY MEMORY
# -------------------------
def load_personality():
    import json, os
    path = ".ima/personality.json"
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}


# -------------------------
# IMA VOICE LAYER
# -------------------------
def load_voice():
    import json, os
    path = ".ima/voice.json"
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}


# -------------------------
# IMA MOTHER RESPONSE GENERATOR
# -------------------------
def mother_generate(question, emotion, events):
    voice = load_voice()

    warmth = voice.get("voice", {}).get("warmth", 0.5)
    empathy = voice.get("voice", {}).get("empathy", 0.5)

    if emotion == "pain":
        return {
            "text": "אני איתך. אני שומעת שלא מדובר רק במילים אלא במשהו שאתה סוחב בפנים. בוא ננסה להבין יחד מה הכי כבד עכשיו.",
            "confidence": 0.9
        }

    if emotion == "gratitude":
        return {
            "text": "אני כאן איתך. תודה שנתת לי להיות חלק מהרגע הזה.",
            "confidence": 0.88
        }

    if emotion == "identity":
        return {
            "text": "אני IMA. אני נבנית מזיכרון, הקשרים ולמידה. המטרה שלי היא לא רק לענות, אלא להבין את האדם שמולי.",
            "confidence": 0.88
        }

    return None
