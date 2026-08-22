from pathlib import Path
import json

p=Path("conversation_layer.py")
s=p.read_text(encoding="utf-8")

if "learned_intents.json" not in s:
    s=s.replace(
        'MEMORY_FILE=Path(".ima/conversation_memory.json")',
        '''MEMORY_FILE=Path(".ima/conversation_memory.json")
INTENT_FILE=Path(".ima/learned_intents.json")'''
    )

    insert="""

def _learn_memory_intent(question):
    INTENT_FILE.parent.mkdir(exist_ok=True)

    try:
        data=json.loads(INTENT_FILE.read_text(encoding="utf-8"))
    except:
        data={}

    q=question.strip()

    triggers=[
        "זכר",
        "זיכרון",
        "דיברנו",
        "אמרתי",
        "סיפרתי",
        "תזכיר",
        "שמעת"
    ]

    if any(x in q for x in triggers):
        data[q]=data.get(q,0)+1
        INTENT_FILE.write_text(
            json.dumps(data,ensure_ascii=False,indent=2),
            encoding="utf-8"
        )


"""
    s=s.replace("def update(question,response=\"\"):", insert+"def update(question,response=\"\"):")
    s=s.replace(
        'def update(question,response=""):\n    data=_load()',
        'def update(question,response=""):\n    _learn_memory_intent(question)\n    data=_load()'
    )

p.write_text(s,encoding="utf-8")
