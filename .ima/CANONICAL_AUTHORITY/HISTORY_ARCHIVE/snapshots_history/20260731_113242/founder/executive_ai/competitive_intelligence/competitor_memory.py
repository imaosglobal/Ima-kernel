import json
from pathlib import Path
import time

FILE=Path("founder/data/competitors.json")


def add_competitor(name, strengths, weaknesses, lessons):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "name":name,
        "strengths":strengths,
        "weaknesses":weaknesses,
        "lessons_for_ima":lessons,
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


def get_competitors():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
