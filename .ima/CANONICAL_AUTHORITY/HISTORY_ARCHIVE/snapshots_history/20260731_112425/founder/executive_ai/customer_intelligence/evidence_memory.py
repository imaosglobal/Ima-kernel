import json
import time
from pathlib import Path

FILE=Path("founder/data/customers/evidence.json")


def add_evidence(company, signal, confidence):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "company":company,
        "signal":signal,
        "confidence":confidence,
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


def get_evidence(company=None):

    if not FILE.exists():
        return []

    data=json.loads(FILE.read_text())

    if company:
        return [
            x for x in data
            if x["company"]==company
        ]

    return data
