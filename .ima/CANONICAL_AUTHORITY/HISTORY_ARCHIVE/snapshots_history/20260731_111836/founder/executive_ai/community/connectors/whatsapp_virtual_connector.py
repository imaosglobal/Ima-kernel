from pathlib import Path
import json
import time
import sys

sys.path.insert(0, ".")

from ima_master_runtime import IMAMaster
from memory.user_memory import remember_user, recall_user

FILE = Path("founder/data/ima_virtual_whatsapp.json")

brain = IMAMaster()


def load():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))

    return {
        "identity": {
            "name": "IMA",
            "platform": "whatsapp_virtual",
            "id": "ima_canonical_001"
        },
        "messages": []
    }


def save(data):
    FILE.parent.mkdir(parents=True, exist_ok=True)

    FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def receive(user, message):

    data = load()

    remember_user(
        user,
        "last_message",
        message
    )

    memory = recall_user(user)

    prompt = (
        f"הקשר משתמש:\n{json.dumps(memory, ensure_ascii=False)}\n\n"
        f"הודעת משתמש:\n{message}"
    )

    event = {
        "from": user,
        "message": message,
        "time": time.time(),
        "status": "received"
    }

    data["messages"].append(event)

    result = brain.ask(prompt)

    reply = result.get(
        "response",
        "IMA לא החזירה תשובה"
    )

    remember_user(
        user,
        "last_response",
        reply
    )

    reply_event = {
        "from": "IMA",
        "message": reply,
        "time": time.time(),
        "status": "sent"
    }

    data["messages"].append(reply_event)

    save(data)

    return reply_event


def identity():
    return load()["identity"]


def inbox():
    return load()["messages"]
