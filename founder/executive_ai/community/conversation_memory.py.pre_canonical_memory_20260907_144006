from pathlib import Path
import json
import time

FILE=Path("founder/data/conversation_memory.json")


def save_message(user,message):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    event={
        "user":user,
        "message":message,
        "time":time.time()
    }

    data.append(event)

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )

    return event


def history():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
