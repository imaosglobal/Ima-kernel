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

try:
    spec=importlib.util.spec_from_file_location(
        'memory_bus_adapter',
        '.ima/runtime/memory_bus_adapter.py'
    )
    memory_bus_adapter=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(memory_bus_adapter)
except Exception:
    memory_bus_adapter=None

try:
    spec=importlib.util.spec_from_file_location(
        'memory_policy_adapter',
        '.ima/runtime/memory_policy_adapter.py'
    )
    memory_policy_adapter=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(memory_policy_adapter)
except Exception:
    memory_policy_adapter=None

MEMORY_FILE=Path(".ima/conversation_memory.json")
INTENT_FILE=Path(".ima/learned_intents.json")

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



def _learn_memory_intent(question):
    from pathlib import Path
    import json

    intent_file = Path(".ima/learned_intents.json")
    intent_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        data=json.loads(intent_file.read_text(encoding="utf-8"))
    except Exception:
        data={}

    q=question.strip()

    data[q]=data.get(q,0)+1

    intent_file.write_text(
        json.dumps(data,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )

    print("[LEARNING]", q)

def update(question,response=""):
    _learn_memory_intent(question)
    data=_load()
    if data and data[-1].get("question")==question:
        data[-1]["response"]=response
    else:
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

    if memory_bus_adapter:
        try:
            memory_bus_adapter.send(
                'conversation_v2',
                {'question': question, 'response': response}
            )
        except Exception:
            pass

    if memory_policy_adapter:
        try:
            memory_policy_adapter.remember(
                'conversation_policy_v1',
                {'question': question, 'response': response}
            )
        except Exception:
            pass

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
