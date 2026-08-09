from pathlib import Path
import json

FILE=Path("founder/data/community_registry.json")


def register(name,platform):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "community":name,
        "platform":platform,
        "active":True
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(data,indent=2,ensure_ascii=False)
    )

    return item
