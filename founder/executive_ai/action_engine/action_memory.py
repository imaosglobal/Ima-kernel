import json
import time
from pathlib import Path


FILE=Path(
"founder/data/action_history.json"
)


def save_action(action,result,lesson=""):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "action":action,
        "result":result,
        "lesson":lesson,
        "time":time.time()
    }

    data.append(item)

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

    return item


def get_actions():

    if FILE.exists():
        return json.loads(
            FILE.read_text()
        )

    return []
