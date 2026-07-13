from pathlib import Path
import json
import time

FILE = Path("founder/data/decisions.json")

def save_decision(decision):
    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    decision["time"]=time.time()

    data.append(decision)

    FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return decision


def history():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return []
