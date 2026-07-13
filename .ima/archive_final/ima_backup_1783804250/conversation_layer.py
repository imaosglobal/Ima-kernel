from pathlib import Path
import json
import identity_context
import time

FILE = Path("conversation_memory.json")

def load():
    if FILE.exists():
        try:
            return json.loads(FILE.read_text(encoding="utf-8"))
        except:
            pass

    return {
        "user": {},
        "history": []
    }


def save(data):
    FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def update(message):
    data = load()

    if "קוראים לי" in message:
        name = message.split("קוראים לי",1)[1].strip().split()[0]
        data["user"]["name"] = name

    if "היוצר" in message or "יוצר שלך" in message:
        data["user"]["relationship"] = "creator"

    data["history"].append({
        "time": int(time.time()),
        "message": message
    })

    data["history"] = data["history"][-20:]

    save(data)
    return data


def context():
    data = load()
    data["identity"] = identity_context.build_context()
    return data
