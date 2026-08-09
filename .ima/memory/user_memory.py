import json
from pathlib import Path

MEM_FILE = Path(".ima/memory.json")

def _load():
    if MEM_FILE.exists():
        return json.loads(MEM_FILE.read_text())
    return {}

def _save(data):
    MEM_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def remember_user(user_id, key, value):
    data = _load()
    if user_id not in data: data[user_id] = {}
    data[user_id][key] = value
    if "history" not in data[user_id]: data[user_id]["history"] = []
    data[user_id]["history"].append({"q": key, "a": value})
    _save(data)
    print(f"REMEMBER {user_id} {key}={value}")

def recall_user(user_id):
    data = _load()
    return data.get(user_id, {"user_id": user_id, "history": []})
