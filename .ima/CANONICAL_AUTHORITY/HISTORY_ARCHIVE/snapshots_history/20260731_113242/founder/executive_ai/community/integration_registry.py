from pathlib import Path
import json

FILE=Path("founder/data/integration_registry.json")


def register(name,category,status="planned"):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "name":name,
        "category":category,
        "status":status
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


def list_integrations():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
