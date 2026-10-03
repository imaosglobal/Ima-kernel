import json
from pathlib import Path
import time
import hashlib
import importlib.util

try:
    spec=importlib.util.spec_from_file_location('memory_bus','.ima/runtime/memory_bus.py')
    memory_bus=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(memory_bus)
except Exception:
    memory_bus=None

MEMORY_ROOT=Path(".ima/conversation_memory")
LEGACY_MEMORY_FILE=Path(".ima/conversation_memory.json")

def _user_key(user_id=None):
    raw=(user_id or "anonymous").strip()
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

def _file(user_id=None):
    return MEMORY_ROOT / f"{_user_key(user_id)}.json"

def _load(user_id=None):
    path=_file(user_id)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    # Legacy memory is not automatically exposed to public users.
    if user_id is None and LEGACY_MEMORY_FILE.exists():
        try:
            return json.loads(LEGACY_MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []

def _save(data,user_id=None):
    path=_file(user_id)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")

def update(question,response="",user_id=None):
    data=_load(user_id)
    data.append({"time":time.time(),"question":question,"response":response})
    _save(data,user_id)
    if memory_bus:
        try:
            memory_bus.log_event("conversation",{"question":question,"response":response,"user_id":user_id or "anonymous"})
        except Exception:
            pass

def context(user_id=None):
    data=_load(user_id)
    return {"count":len(data),"recent":data[-10:],"user_id":user_id or "anonymous"}

def recall(query,user_id=None):
    data=_load(user_id)
    q=query.lower().strip()
    if not q:
        filtered=[x for x in reversed(data) if x.get("response","").strip()][:10]
        return list(reversed(filtered))

    memory_commands=["מה אתה זוכר","מה את זוכרת","זיכרון","תזכיר לי","מה דיברנו","היסטוריה"]
    if any(cmd in q for cmd in memory_commands):
        filtered=[]
        for item in reversed(data):
            response=item.get("response","").strip()
            question=item.get("question","").strip()
            if not response or any(cmd in question for cmd in memory_commands):
                continue
            filtered.append(item)
            if len(filtered)>=10: break
        return list(reversed(filtered))

    words=[w for w in q.split() if len(w)>2]
    results=[]
    for item in data:
        text=(item.get("question","")+" "+item.get("response","")).lower()
        score=sum(1 for w in words if w in text)
        if score>0 and item.get("response","").strip():
            item=dict(item); item["_score"]=score; results.append(item)
    results.sort(key=lambda x:x.get("_score",0),reverse=True)
    return results[:5]
