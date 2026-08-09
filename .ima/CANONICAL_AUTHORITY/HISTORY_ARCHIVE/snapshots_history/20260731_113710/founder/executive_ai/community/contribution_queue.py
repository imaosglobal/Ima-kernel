from pathlib import Path
import json
import time

FILE=Path("founder/data/community_queue.json")


def add_proposal(source,content):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "id":time.time(),
        "source":source,
        "content":content,
        "status":"pending"
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)
    FILE.write_text(
        json.dumps(data,indent=2,ensure_ascii=False)
    )

    return item


def pending():

    if FILE.exists():
        return [
            x for x in json.loads(FILE.read_text())
            if x["status"]=="pending"
        ]

    return []
