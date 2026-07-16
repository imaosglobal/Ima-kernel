import time
import json
from pathlib import Path

LOG = Path(".ima/brain_sync.jsonl")


BRAINS = []


def register(name, brain):
    BRAINS.append({
        "name": name,
        "brain": brain
    })


def broadcast(event):

    LOG.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(LOG,"a") as f:
        f.write(
            json.dumps(event,ensure_ascii=False)
            +"\n"
        )

    results=[]

    for item in BRAINS:
        try:
            obj=item["brain"]

            if hasattr(obj,"learn"):
                results.append(
                    item["name"]+":learn"
                )

        except Exception:
            pass

    return results


def status():
    return [
        x["name"]
        for x in BRAINS
    ]
