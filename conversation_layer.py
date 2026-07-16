import json
from pathlib import Path
import time
import importlib.util

try:
    spec=importlib.util.spec_from_file_location('memory_bus','.ima/runtime/memory_bus.py')
    memory_bus=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(memory_bus)
except Exception:
    memory_bus=None

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

    if memory_bus:
        try:
            memory_bus.log_event('conversation', {'question': question, 'response': response})
        except Exception:
            pass

def context():
    data=_load()
    return {
        "count":len(data),
        "recent":data[-10:]
    }

def recall(query):
    data = _load()

    q = query.lower().strip()

    # empty query = return recent real conversations
    if not q:
        filtered=[]
        for item in reversed(data):
            if item.get("response","").strip():
                filtered.append(item)
            if len(filtered) >= 10:
                break
        return list(reversed(filtered))

    memory_commands = [
        "מה אתה זוכר",
        "מה את זוכרת",
        "זיכרון",
        "תזכיר לי",
        "מה דיברנו",
        "היסטוריה"
    ]

    if any(cmd in q for cmd in memory_commands):
        filtered = []

        for item in reversed(data):
            response = item.get("response","").strip()
            question = item.get("question","").strip()

            if not response:
                continue

            if any(cmd in question for cmd in memory_commands):
                continue

            if response.startswith("אני כאן, אורי. שמעתי אותך"):
                continue

            filtered.append(item)

            if len(filtered) >= 10:
                break

        return list(reversed(filtered))

    results = []

    words = [w for w in q.split() if len(w) > 2]

    for item in data:
        text = (
            item.get("question","")
            + " "
            + item.get("response","")
        ).lower()

        score = sum(1 for w in words if w in text)

        if score > 0:
            item["_score"] = score
            results.append(item)

    results = [
        x for x in results
        if x.get("response","").strip()
        and not x.get("response","").startswith("אני כאן, אורי. שמעתי אותך")
        and not x.get("response","").startswith("אני איתך.")
    ]

    results.sort(
        key=lambda x:x.get("_score",0),
        reverse=True
    )

    return results[:5]

