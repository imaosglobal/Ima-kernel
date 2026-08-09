from pathlib import Path
import json,time

p=Path("conversation_layer.py")

code=r'''
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
    q=query.lower()
    results=[]
    for item in data:
        text=(item.get("question","")+" "+item.get("response","")).lower()
        if q in text:
            results.append(item)
    return results[-5:]
'''

p.write_text(code.strip(),encoding="utf-8")

print("[OK] MEMORY LAYER REPAIRED")
