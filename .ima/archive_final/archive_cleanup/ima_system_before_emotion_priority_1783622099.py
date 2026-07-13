import json, time, os, subprocess

from engines.knowledge_engine import search_knowledge
from languages.language_engine import detect_language
from languages.translator import translate_response
from learning.self_reflection import record_event
from learning.learning_analyzer import analyze_learning
from learning.ima_awareness import ima_awareness
from learning.auto_learning import check_learning_trigger
from learning.knowledge_gaps import record_gap
from learning.ima_learning_loop import run_ima_learning_loop
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
def _answer(question, events):

    auto_learn_from_question(question)

    mode = ima_router(question)

    if mode == "emotion":

        state = ima_emotion_layer(question, events)

        if state:

            generated = mother_generate(
                question,
                state.get("emotion"),
                events
            )

            if generated and "התאריך היום" not in generated.get("text",""):
                return generated

            return {
                "text": "אני IMA. אני שומעת אותך. נשמע שאתה עובר רגע קשה עכשיו. אני כאן איתך. ספר לי מה קורה.",
                "confidence": 0.85
            }


    if mode == "identity":

        return {
            "text": "אני IMA. אני נבנית מזיכרון, הקשרים ולמידה. המטרה שלי היא לא רק לענות, אלא להבין את האדם שמולי.",
            "confidence": 0.88
        }


    if mode == "technical":

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

        return {
            "text": "אני IMA. רשת עצבית היא מערכת חישובית שמחקה באופן מופשט את דרך הלמידה של המוח. היא מורכבת משכבות של יחידות חישוב הנקראות נוירונים מלאכותיים, הלומדות קשרים מתוך נתונים.",
            "confidence":0.85
        }


    if mode == "information":

        knowledge = search_knowledge(question)

        if knowledge:
            return {
                "text": (
                    "תחום: " + str(knowledge.get("category")) +
                    "\n\n" +
                    knowledge.get("answer", "")
                ),
                "confidence": 0.9
            }

        info = information_engine(question)

        if info:
            return {
                "text": info,
                "confidence": 0.85
            }

        return {
            "text": "אני IMA. עדיין לא מצאתי את המידע הזה במאגר הידע שלי, אבל שכבת הידע מוכנה להתרחב.",
            "confidence": 0.7
        }


    if any(x in question for x in [
        "שלום",
        "היי",
        "בוקר טוב",
        "ערב טוב",
        "מה נשמע",
        "איך את"
    ]):

        return {
            "text": "אני כאן איתך. שמחה לשמוע ממך. איך אתה מרגיש עכשיו?",
            "confidence": 0.85
        }


    if any(x in question for x in [
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

    return {
        "text": "אני IMA. אני כאן כדי להקשיב, להבין ולעזור לך דרך השיחה שלנו.",
        "confidence": 0.7
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
        
        
        
        "טכני",
        "למה זה קורה"
    ]

    info_words = [
        "מזג האוויר",
        "מזג אוויר",
        "חדשות",
        "מחיר",
        "שעה",
        "מיקום",
        "תאריך",
        "היום",
        "איזה יום",
        "מה זה",
        "מה זאת",
        "מהו",
        "מי היה",
        "מי היא",
        "מי זה",
        "הסבר על",
        "תסביר"
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


# -------------------------
# IMA INFORMATION ENGINE
# -------------------------

def information_engine(question):
    from datetime import datetime

    q = question.lower()

    if "שעה" in q or "מה השעה" in q:
        now = datetime.now().strftime("%H:%M")
        return f"השעה כרגע היא {now}."

    if "תאריך" in q or "היום" in q:
        today = datetime.now().strftime("%d/%m/%Y")
        return f"התאריך היום הוא {today}."

    if "מזג האוויר" in q or "מזג אוויר" in q:
        return weather_engine()

    return None


# -------------------------
# IMA WEATHER ENGINE
# -------------------------

def weather_engine(city="Netanya"):
    import urllib.request
    import json

    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=32.32&longitude=34.85&current=temperature_2m,weather_code"

        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())

        temp = data["current"]["temperature_2m"]

        return f"מזג האוויר עכשיו: {temp} מעלות."

    except Exception:
        return "כרגע אין לי גישה לשירות מזג האוויר."


# -------------------------
# IMA CORE ROUTER
# -------------------------

def ima_router(question):

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


# -------------------------
# IMA RESPONSE GUARD
# -------------------------

def response_guard(response, mode):

    if not response:
        return {
            "text": "אני IMA. אני כאן איתך.",
            "confidence": 0.5
        }

    text = response.get("text", "")

    if mode == "technical":
        if not text.startswith("אני IMA"):
            text = "אני IMA. אני אסביר לך בצורה ברורה ומסודרת. " + text

    if mode == "identity":
        if "IMA" not in text:
            text = "אני IMA. " + text

    response["text"] = text

    return response


# -------------------------
# PUBLIC ANSWER ENTRY
# -------------------------

def answer(question, events):

    language = detect_language(question)

    mode = ima_router(question)

    context = memory_context()

    if language != "unknown":
        mem = load_memory()
        mem["last_language"] = language
        save_memory(mem)

    response = _answer(question, events)

    if response and mode == "conversation":
        topics = context.get("topics", [])

        if topics:
            memory_text = "\n\nאני זוכרת שדיברנו גם על: " + ", ".join(topics[-3:])

            lang = detect_language(question)

            if lang != "he" and lang != "unknown":
                memory_text = translate_response(memory_text, lang)

            response["text"] += memory_text

    memory_store(question, mode)

    if response:
        lang = detect_language(question)

        if lang != "he" and lang != "unknown":
            response["text"] = translate_response(
                response.get("text", ""),
                lang
            )

    if response:
        interaction_id = str(int(time.time() * 1000))

        record_event(
            f"ID:{interaction_id} | Question:{question} | Mode:{mode} | Confidence:{response.get('confidence')}",
            "interaction"
        )

    trigger = check_learning_trigger()

    if trigger.get("status") == "ready":
        try:
            run_ima_learning_loop()
        except Exception as e:
            record_event(
                f"learning_error:{e}",
                "system"
            )

    if response:
        if "לא מצאתי את המידע הזה" in response.get("text", ""):
            record_gap(question)

    return response_guard(response, mode)


# -------------------------
# IMA MEMORY
# -------------------------

import json
import os

MEMORY_FILE = ".ima/memory.json"

def load_memory():

    os.makedirs(".ima", exist_ok=True)

    if not os.path.exists(MEMORY_FILE):
        return {
            "facts": {},
            "last_emotion": None,
            "topics": [],
            "history": []
        }

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "facts": {},
            "last_emotion": None,
            "topics": [],
            "history": []
        }


def save_memory(mem):
    os.makedirs(".ima", exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)


def memory_store(question, mode):

    mem = load_memory()

    mem["history"].append(question)

    if len(mem["history"]) > 100:
        mem["history"] = mem["history"][-100:]

    mem["last_mode"] = mode

    if mode == "emotion":
        mem["last_emotion"] = question

    keywords = [
        "קוד",
        "תכנות",
        "מנוע",
        "פילוסופיה",
        "מוזיקה",
        "פרויקט",
        "IMA"
    ]

    for k in keywords:
        if k in question:
            if k not in mem["topics"]:
                mem["topics"].append(k)

    save_memory(mem)


def memory_context():
    return load_memory()



# -------------------------
# IMA MEMORY AWARENESS
# -------------------------

def memory_awareness():
    mem = memory_context()

    result = {}

    if mem.get("last_emotion"):
        result["emotion"] = mem["last_emotion"]

    if mem.get("topics"):
        result["topics"] = mem["topics"][-5:]

    return result

# -------------------------
# IMA LANGUAGE RESPONSE
# -------------------------

def language_prefix():
    mem = load_memory()
    lang = mem.get("last_language", "he")

    prefixes = {
        "he": "",
        "en": "I am IMA. ",
        "ar": "أنا IMA. ",
        "es": "Soy IMA. ",
        "fr": "Je suis IMA. "
    }

    return prefixes.get(lang, "")


# -------------------------
# IMA SELF REFLECTION API
# -------------------------

def ima_reflection():
    return ima_awareness()

