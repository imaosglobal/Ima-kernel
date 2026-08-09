from fastapi import FastAPI
from pydantic import BaseModel
from startup.pitch_engine import PitchEngine
from startup.fundraising_engine import FundraisingEngine
from startup.toolbox_engine import ToolboxEngine
from startup.knowledge_engine import KnowledgeEngine
from startup.input_buffer import InputBuffer

app = FastAPI()
PITCH_ENGINE = PitchEngine()
FUND_ENGINE = FundraisingEngine()
TOOLBOX = ToolboxEngine()
KNOWLEDGE = KnowledgeEngine()
INPUT_BUFFER = InputBuffer()

def handle_command(text):
    raw = text.strip()
    if raw.startswith("אתה: "): raw = raw[5:]

    # ניהול קבצים וקוד רב שורה
    result = INPUT_BUFFER.add(raw)

    if INPUT_BUFFER.active:
        return ""

    if result is not None and result != raw:
        return process_input(result)

    raw = result

    t = raw.lower()
    if "מה יש לך" in t or "מה אתה יודע" in t: return KNOWLEDGE.answer(t)
    if "toolbox" in t: return KNOWLEDGE.answer("toolbox")
    if "deck" in t: return PITCH_ENGINE.build_deck()
    if "term sheet" in t: return FUND_ENGINE.generate_term_sheet()
    if "runway" in t: return FUND_ENGINE.calculate_runway()
    return process_input(raw)



def process_input(text):
    """
    כאן מתחבר המוח האמיתי.
    אין תשובה מתוכנתת.
    """
    try:
        if "KNOWLEDGE" in globals():
            answer=KNOWLEDGE.answer(text)
            if answer:
                return answer
    except Exception:
        pass

    return text


def smart_reply(text):
    """
    שכבת שיחה.
    אין תשובות מוכנות.
    מחזיר הקשר מהזיכרון בלבד.
    """
    text=text.strip()

    if not text:
        return ""

    # שאלות על קבצים
    if "מה יש" in text or "מה את יודעת" in text:
        return KNOWLEDGE.answer(text)

    # חיפוש בפרויקט
    try:
        found=[]
        for k,v in KNOWLEDGE.memory.items():
            if any(x in v.lower() for x in text.lower().split()):
                found.append(k)
        if found:
            return "מצאתי בזיכרון:\n" + "\n".join(found[:5])
    except:
        pass

    return "קיבלתי. אני מחברת את זה להקשר הפרויקט ולזיכרון שלי."

class Message(BaseModel): text: str
@app.post("/chat")
def chat(msg: Message):
    reply = handle_command(msg.text)
    return {"reply": "אמא: " + reply} if reply else {"reply": ""}
