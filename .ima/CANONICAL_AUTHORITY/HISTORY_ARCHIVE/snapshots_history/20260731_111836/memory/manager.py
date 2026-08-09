from pathlib import Path
import json,time

FILE=Path(".ima/user_memory.json")

def remember(key,value):
    data={}

    if FILE.exists():
        data=json.loads(FILE.read_text())

    data[key]={
        "value":value,
        "time":time.time()
    }

    FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return data


def recall():
    if FILE.exists():
        return json.loads(FILE.read_text())

    return {}
