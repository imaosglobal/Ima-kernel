import json
import time
from pathlib import Path

FILE=Path("founder/data/customers/outreach_history.json")


def save_outreach(company, status, lesson=""):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "company":company,
        "status":status,
        "lesson":lesson,
        "time":time.time()
    }

    data.append(item)

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return item


def history():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
