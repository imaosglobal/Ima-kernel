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

    # אם זה בתוך איסוף קובץ
    result = INPUT_BUFFER.add(raw)
    if INPUT_BUFFER.active:
        return ""

    if result != raw:
        return f"קיבלתי קובץ עם {len(result.split())} מילים 💛 שמרתי לזיכרון"

    raw = result
    if result != raw:
        return f"קיבלתי קובץ עם {len(result.split())} מילים 💛 שמרתי לזיכרון"

    raw = result

    t = raw.lower()
    if "מה יש לך" in t or "מה אתה יודע" in t: return KNOWLEDGE.answer(t)
    if "toolbox" in t: return KNOWLEDGE.answer("toolbox")
    if "deck" in t: return PITCH_ENGINE.build_deck()
    if "term sheet" in t: return FUND_ENGINE.generate_term_sheet()
    if "runway" in t: return FUND_ENGINE.calculate_runway()
    return f"קיבלתי: {raw} 💛"

class Message(BaseModel): text: str
@app.post("/chat")
def chat(msg: Message):
    reply = handle_command(msg.text)
    return {"reply": "אמא: " + reply} if reply else {"reply": ""}
