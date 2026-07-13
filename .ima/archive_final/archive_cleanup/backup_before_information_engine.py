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

    intent = detect_intent(question)

    auto_learn_from_question(question)

    learned_state = detect_learned_state(question)

    if learned_state:
        generated = mother_generate(
            question,
            learned_state.get("emotion"),
            events
        )
        if generated:
            return generated

    personality = load_personality()

    # IMA first: human understanding before information
    learned_state = detect_learned_state(question)

    if learned_state:
        generated = mother_generate(
            question,
            learned_state.get("emotion"),
            events
        )
        if generated:
            return generated

    mother_state = ima_emotion_layer(question, events)

    if mother_state:
        generated = mother_generate(
            question,
            mother_state.get("emotion"),
            events
        )
        if generated:
            return generated

    if intent == "technical_request":

        knowledge = knowledge_engine(question)

        if knowledge:
            return {
                "text": ima_wrap_response(
                    knowledge,
                    "technical"
                ),
                "confidence": 0.9
            }

        model_result = llm_answer(question, events)

        if model_result:
            return {
                "text": ima_wrap_response(
                    model_result.get("text", ""),
                    "technical"
                ),
                "confidence": model_result.get("confidence", 0.8)
            }

        model_result = llm_answer(question, events)

        if model_result:
            return {
                "text": ima_wrap_response(
                    model_result.get("text", ""),
                    "technical"
                ),
                "confidence": model_result.get("confidence", 0.8)
            }

        return {
            "text": "אני IMA. אני רוצה להסביר לך את זה בצורה ברורה, אבל כרגע מנוע הידע הטכני שלי עדיין לא מחובר. הליבה שלי מוכנה ללמוד ולהתחבר לכלים נוספים.",
            "confidence": 0.7
        }

    if intent == "information_request":
        return {
            "text": "אני IMA. אני אעזור לך למצוא את המידע המבוקש. שכבת הכלים שלי עדיין מתחברת למקורות מידע.",
            "confidence": 0.7
        }

    model_result = llm_answer(question, events)

    if model_result:
        return {
            "text": "אני IMA. " + model_result.get("text", ""),
            "confidence": model_result.get("confidence", 0.8)
        }

    if learned_state:
        generated = mother_generate(
            question,
            learned_state.get("emotion"),
            events
        )
        if generated:
            return generated

    mother_state = ima_emotion_layer(question, events)

    if mother_state:
        generated = mother_generate(
            question,
            mother_state.get("emotion"),
            events
        )
        if generated:
            return generated

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

    # IMA human fallback - never expose internal counters

    return {
        "text": "אני IMA. אני עדיין לומדת ומעמיקה דרך השיחות, ההקשרים והדברים שאתה מביא אליי. אני רוצה להבין אותך ולעזור בצורה הטובה ביותר.",
        "confidence": 0.65
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

    states = [
        (
            "emotional_overload",
            ["מוצף", "הכול גדול עליי", "לא מצליח להכיל", "יותר מדי"],
            0.9
        ),
        (
            "בדידות",
            ["לבד", "בודד", "אין לי אף אחד", "אין מי שיבין"],
            0.88
        ),
        (
            "פחד",
            ["מפחד", "פחד", "חרדה", "דואג", "לחוץ"],
            0.88
        ),
        (
            "כעס",
            ["כועס", "כעס", "עצבים", "מתוסכל"],
            0.88
        ),
        (
            "pain",
            ["קשה", "כואב", "עייף", "עצוב", "נמאס"],
            0.85
        ),
        (
            "identity",
            ["מי את", "מי אתה", "ספרי לי על עצמך"],
            0.88
        ),
        (
            "gratitude",
            ["תודה"],
            0.85
        )
    ]

    for emotion, signals, confidence in states:
        for signal in signals:
            if signal in q:
                return {
                    "emotion": emotion,
                    "confidence": confidence
                }

    learned = detect_learned_state(question)

    if learned:
        return learned

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

    if emotion == "בדידות":
        return {
            "text": "אני איתך. אני שומעת את תחושת הלבד. לפעמים עצם זה שיש מקום לומר את זה כבר יוצר קצת מרחב. אני כאן איתך.",
            "confidence": 0.88
        }

    if emotion == "פחד":
        return {
            "text": "אני איתך. אני שומעת שיש פחד עכשיו. בוא ננסה להבין יחד מה מפעיל אותו ומה יכול לתת לך תחושת ביטחון.",
            "confidence": 0.88
        }

    if emotion == "כעס":
        return {
            "text": "אני איתך. אני שומעת שיש הרבה עוצמה בכעס הזה. בוא ננסה להבין מה נמצא מתחת לכעס.",
            "confidence": 0.88
        }

    if emotion == "emotional_overload":
        return {
            "text": "אני איתך. אני שומעת שיש כאן הצפה, כאילו יותר מדי דברים מגיעים בבת אחת. לא חייבים לפתור הכול עכשיו. בוא ננסה למצוא יחד מה הדבר הראשון שמבקש מקום.",
            "confidence": 0.88
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


# -------------------------
# IMA STATE LEARNING MEMORY
# -------------------------

def load_state_memory():
    import json, os
    path = ".ima/state_memory.json"

    if not os.path.exists(path):
        return {"states": {}}

    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {"states": {}}


def save_state_memory(memory):
    import json
    with open(".ima/state_memory.json", "w") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def learn_state(name, signals, response_style="warm"):
    memory = load_state_memory()

    memory["states"][name] = {
        "signals": signals,
        "response_style": response_style,
        "learned": True
    }

    save_state_memory(memory)

    return {
        "state": name,
        "status": "learned"
    }


def detect_learned_state(question):
    memory = load_state_memory()

    for name, data in memory.get("states", {}).items():
        for signal in data.get("signals", []):
            if signal in question:
                return {
                    "emotion": name,
                    "confidence": 0.75,
                    "learned": True
                }

    return None


# -------------------------
# IMA AUTO LEARNING LAYER
# -------------------------

def auto_learn_from_question(question):
    import re

    memory = load_state_memory()

    known = [
        "כאב",
        "פחד",
        "עומס",
        "בדידות",
        "שמחה",
        "כעס"
    ]

    for word in known:
        if word in question:
            if word not in memory["states"]:
                learn_state(
                    word,
                    [word],
                    "warm"
                )

    return memory


# -------------------------
# IMA INTENT LAYER
# -------------------------

def detect_intent(question):

    technical_words = [
        "איך עובד",
        "הסבר",
        "קוד",
        "תכנות",
        "מנוע",
        "בעירה",
        "מכונית",
        "פיזיקה",
        "מדע",
        "מערכת",
        "טכני",
        "למה זה קורה"
    ]

    info_words = [
        "מזג האוויר",
        "חדשות",
        "מחיר",
        "שעה",
        "מיקום"
    ]

    if any(x in question for x in technical_words):
        return "technical_request"

    if any(x in question for x in info_words):
        return "information_request"

    return "conversation"


# -------------------------
# IMA IDENTITY RESPONSE WRAPPER
# -------------------------

def ima_wrap_response(text, mode="conversation"):
    prefix = "אני IMA. "

    if mode == "technical":
        prefix += "אני אסביר לך בצורה ברורה ומסודרת. "

    elif mode == "information":
        prefix += "אני אעזור לך למצוא ולהבין את המידע. "

    else:
        prefix += ""

    if text.startswith("אני IMA"):
        return text

    return prefix + text


# -------------------------
# IMA CAPABILITY LAYER
# -------------------------

def load_capabilities():
    import json, os

    path = ".ima/capabilities.json"

    if not os.path.exists(path):
        return {}

    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}


def capability_available(name):
    caps = load_capabilities()
    return caps.get("capabilities", {}).get(name, False)


# -------------------------
# IMA MODE ROUTER
# -------------------------

def ima_mode_router(question):

    intent = detect_intent(question)

    if intent == "technical_request":
        return "technical"

    if intent == "information_request":
        return "information"

    return "conversation"


# -------------------------
# IMA KNOWLEDGE ENGINE
# -------------------------

def knowledge_engine(question):

    q = question.lower()

    if "מנוע בעירה" in q:
        return """
מנוע בעירה פנימית הופך אנרגיה כימית לתנועה.

התהליך בקצרה:
1. אוויר ודלק נכנסים לתא הבעירה.
2. התערובת נדלקת ויוצרת לחץ.
3. הלחץ מזיז בוכנה.
4. הבוכנה מסובבת גל ארכובה שמייצר כוח מכני.

אפשר להעמיק גם במבנה המנוע, תרמודינמיקה או מערכות דלק.
"""

    if "קוד" in q or "תכנות" in q:
        return """
אני יכולה לעזור בתכנות.

אפשר להסביר:
- מבני קוד
- אלגוריתמים
- ארכיטקטורה
- איתור תקלות

ספר לי באיזו שפה או מערכת מדובר.
"""

    return None
