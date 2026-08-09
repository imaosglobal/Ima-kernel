
import json
import hashlib
import time
from pathlib import Path

FILE=Path("learning/user_memory.json")


def load():
    if FILE.exists():
        try:
            return json.loads(FILE.read_text())
        except:
            pass

    return {"users":{}}


def _event_hash(data):
    clean={
        k:v for k,v in data.items()
        if not k.startswith("_")
    }

    raw=json.dumps(
        clean,
        ensure_ascii=False,
        sort_keys=True
    )

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()


def learn(user_id, data):

    memory=load()

    if user_id not in memory["users"]:
        memory["users"][user_id]=[]


    event_id=_event_hash(data)


    for item in memory["users"][user_id]:
        if item.get("_id")==event_id:
            item["last_seen"]=time.time()
            FILE.write_text(
                json.dumps(
                    memory,
                    ensure_ascii=False,
                    indent=2
                )
            )
            return memory["users"][user_id]


    data["_id"]=event_id
    data["_created"]=time.time()
    data["_last_seen"]=time.time()

    memory["users"][user_id].append(data)


    FILE.write_text(
        json.dumps(
            memory,
            ensure_ascii=False,
            indent=2
        )
    )


    return memory["users"][user_id]
