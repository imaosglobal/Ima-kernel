import json
from pathlib import Path

MEM_FILE = Path.home() / ".ima/user_memory.json"

def _load():
    if not MEM_FILE.exists():
        return {}
    return json.loads(MEM_FILE.read_text(encoding="utf-8"))

def _save(data):
    MEM_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEM_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def remember_user(user_id, key, value):
    data = _load()
    if user_id not in data:
        data[user_id] = {"history": []}
    data[user_id][key] = value
    # שומר גם בהיסטוריה
    if key == "last_message":
        data[user_id]["history"].append(value)
    _save(data)

def recall_user(user_id):
    data = _load()
    return data.get(user_id, {"history": []})
