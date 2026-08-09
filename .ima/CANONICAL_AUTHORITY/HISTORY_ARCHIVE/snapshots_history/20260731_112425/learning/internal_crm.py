import json
import time
from pathlib import Path

FILE=Path("learning/internal_crm.json")


def load():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf8"))

    return {
        "users": {},
        "events": []
    }


def register_user(user_id, profile=None):

    data=load()

    if user_id not in data["users"]:
        data["users"][user_id]={
            "profile": profile or {},
            "created": time.time(),
            "history":[]
        }

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    return data["users"][user_id]


def add_event(user_id,event):

    data=load()

    if user_id not in data["users"]:
        register_user(user_id)

    record={
        "time":time.time(),
        "user":user_id,
        "event":event
    }

    data["events"].append(record)
    data["users"][user_id]["history"].append(record)

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    return record
