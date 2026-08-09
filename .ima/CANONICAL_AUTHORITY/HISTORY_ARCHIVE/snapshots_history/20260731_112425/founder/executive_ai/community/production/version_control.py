from pathlib import Path
import json,time

FILE=Path("founder/data/community_versions.json")


def create_version(component,change):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "id":time.time(),
        "component":component,
        "change":change
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(data,indent=2)
    )

    return item
