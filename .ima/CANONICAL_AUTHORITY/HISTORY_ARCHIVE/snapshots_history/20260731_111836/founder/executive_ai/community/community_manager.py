from pathlib import Path
import json
import time

FILE=Path("founder/data/community_v2.json")


def load():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return {
        "communities":[],
        "members":[],
        "roles":[]
    }


def save(data):

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


def create(name, category):

    data=load()

    item={
        "id":name.lower().replace(" ","_"),
        "name":name,
        "category":category,
        "created":time.time()
    }

    data["communities"].append(item)

    save(data)

    return item
