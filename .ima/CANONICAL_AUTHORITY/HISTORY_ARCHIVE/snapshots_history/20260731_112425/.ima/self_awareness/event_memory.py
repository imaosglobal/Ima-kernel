import json
import time
from pathlib import Path

LOG=Path(".ima/self_awareness/events.jsonl")

def record(event, data=None):
    item={
        "time":time.strftime("%Y-%m-%d %H:%M:%S"),
        "event":event,
        "data":data or {}
    }

    LOG.parent.mkdir(exist_ok=True)

    with open(LOG,"a") as f:
        f.write(json.dumps(item,ensure_ascii=False)+"\n")

def latest(n=10):
    if not LOG.exists():
        return []

    lines=LOG.read_text().splitlines()

    return [
        json.loads(x)
        for x in lines[-n:]
    ]


if __name__=="__main__":
    record(
        "observer_initialized",
        {"status":"online"}
    )

    print(latest())
