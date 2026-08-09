from pathlib import Path
import json
import time

FILE = Path(".ima/users_memory.json")


def load():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    return {"users": {}}


def save(data):
    FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def remember_user(user_id, key, value):
    data = load()

    if user_id not in data["users"]:
        data["users"][user_id] = {}

    data["users"][user_id][key] = {
        "value": value,
        "time": time.time()
    }

    save(data)
    return data["users"][user_id]


def recall_user(user_id):
    data = load()
    return data["users"].get(user_id, {})
