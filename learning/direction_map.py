"""User-controlled direction-map runtime for IMA.

This module stores only explicitly submitted direction data. It does not infer identity
or vocation and does not replace the existing conversation-memory system.
"""
from __future__ import annotations
import copy, hashlib, json, time
from pathlib import Path

STORE = Path(__file__).resolve().parent / ".ima" / "direction_maps.json"
CATEGORIES = [
    "values","strengths","needs","interests","protective_commitments","concerns",
    "relationships","creations","contribution_hypotheses","constraints","experiments",
    "evidence","direction_hypotheses","counterevidence","open_questions",
]

def _load():
    if not STORE.exists():
        return {}
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _save(data):
    STORE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STORE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STORE)

def _owner(user_id):
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:32]

def empty(user_id):
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return {"schema_version":"1.0.0","owner":_owner(user_id),"updated_at":now,
            **{k:[] for k in CATEGORIES}}

def get(user_id):
    data=_load()
    return copy.deepcopy(data.get(_owner(user_id), empty(user_id)))

def replace(user_id, direction_map):
    if not isinstance(direction_map, dict):
        raise ValueError("direction map must be an object")
    result=empty(user_id)
    for key in CATEGORIES:
        value=direction_map.get(key, [])
        if not isinstance(value, list):
            raise ValueError(f"{key} must be an array")
        result[key]=value
    result["updated_at"]=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _load_data=_load()
    _load_data[_owner(user_id)]=result
    _save(_load_data)
    return copy.deepcopy(result)

def add_entry(user_id, category, entry):
    if category not in CATEGORIES:
        raise ValueError("unknown direction category")
    if not isinstance(entry, dict) or not isinstance(entry.get("content"), str) or not entry["content"].strip():
        raise ValueError("entry.content is required")
    item=dict(entry)
    item.setdefault("id", hashlib.sha256((user_id+category+item["content"]+str(time.time_ns())).encode()).hexdigest()[:24])
    item.setdefault("status", "FIRST_PERSON_REPORT")
    item.setdefault("provenance", "user_explicit")
    item.setdefault("created_at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    current=get(user_id)
    current[category].append(item)
    return replace(user_id, current)

def delete_entry(user_id, category, entry_id):
    if category not in CATEGORIES:
        raise ValueError("unknown direction category")
    current=get(user_id)
    before=len(current[category])
    current[category]=[x for x in current[category] if x.get("id") != entry_id]
    if len(current[category]) == before:
        return False, current
    replace(user_id,current)
    return True,current
