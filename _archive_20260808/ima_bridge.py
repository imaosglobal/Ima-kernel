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
    raw=text.strip()

    if raw.startswith("אתה: "):
        raw=raw[5:]

    result=INPUT_BUFFER.add(raw)

    if INPUT_BUFFER.active:
        return ""

    if result is not None and result != raw:
        return "קיבלתי תוכן רב שורה לעיבוד 💛"

    raw=result

    return smart_reply(raw)



def smart_reply(text):

    t=text.strip()

    if not t:
        return ""

    # חיפוש מידע רק כשמבקשים מידע
    if any(x in t.lower() for x in [
        "מה יש",
        "מה כתוב",
        "איפה",
        "חפש",
        "קובץ",
        "toolbox",
        "deck"
    ]):
        try:
            return KNOWLEDGE.answer(t)
        except Exception as e:
            return "שגיאת זיכרון: "+str(e)

    # שיחה רגילה
    return "שמעתי אותך: " + t



class Message(BaseModel): text: str
@app.post("/chat")
def chat(msg: Message):
    reply = handle_command(msg.text)
    return {"reply": "אמא: " + reply} if reply else {"reply": ""}
