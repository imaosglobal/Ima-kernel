
import json
import time
from pathlib import Path


FILE=Path(
"founder/data/world_opportunities.json"
)


def save_entity(entity):

    data=[]

    if FILE.exists():
        data=json.loads(
            FILE.read_text()
        )

    entity["discovered_at"]=time.time()

    data.append(entity)

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return entity


def get_entities():

    if FILE.exists():
        return json.loads(
            FILE.read_text()
        )

    return []
