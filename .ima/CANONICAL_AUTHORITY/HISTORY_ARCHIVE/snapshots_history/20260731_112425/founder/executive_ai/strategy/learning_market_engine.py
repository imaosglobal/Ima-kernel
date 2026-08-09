import json
from pathlib import Path
import time

FILE=Path("founder/data/market_learning.json")


def learn_from_signal(signal):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    signal["time"]=time.time()

    data.append(signal)

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return signal


def market_memory():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
