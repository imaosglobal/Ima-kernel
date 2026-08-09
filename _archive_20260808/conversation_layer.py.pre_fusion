import json
from pathlib import Path
import time

MEMORY_FILE=Path(".ima/conversation_memory.json")

def _load():
    if not MEMORY_FILE.exists():
        return []
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except:
        return []

def _save(data):
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    MEMORY_FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )

def update(question,response=""):
    data=_load()
    data.append({
        "time":time.time(),
        "question":question,
        "response":response
    })
    _save(data)

def context():
    data=_load()
    return {
        "count":len(data),
        "recent":data[-10:]
    }

def recall(query):
    data=_load()

    q=query.lower().strip()

    memory_commands=[
        "מה אתה זוכר",
        "מה את זוכרת",
        "זיכרון",
        "תזכיר לי",
        "מה דיברנו",
        "היסטוריה"
    ]

    if any(cmd in q for cmd in memory_commands):
        return data[-10:]

    results=[]
    words=[w for w in q.split() if len(w)>2]

    for item in data:
        text=(
            item.get("question","")
            +" "
            +item.get("response","")
        ).lower()

        score=sum(1 for w in words if w in text)

        if score>0:
            item["_score"]=score
            results.append(item)

    results.sort(
        key=lambda x:x.get("_score",0),
        reverse=True
    )

    return results[:5]
