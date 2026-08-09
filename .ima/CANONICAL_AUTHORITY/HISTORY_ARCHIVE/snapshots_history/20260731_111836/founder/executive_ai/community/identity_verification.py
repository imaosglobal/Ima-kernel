from pathlib import Path
import json

FILE=Path("founder/data/identity_registry.json")


def load():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []


def register(identity_id,name):

    data=load()

    item={
        "id":identity_id,
        "name":name,
        "verified":True
    }

    data.append(item)

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

    return item


def verify(identity_id):

    for item in load():

        if item["id"]==identity_id:
            return True

    return False
