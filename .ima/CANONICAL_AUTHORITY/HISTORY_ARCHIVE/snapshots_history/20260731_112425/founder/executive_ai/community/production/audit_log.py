from pathlib import Path
import json,time

FILE=Path("founder/data/audit_log.json")

def record(event,data):

    logs=[]

    if FILE.exists():
        logs=json.loads(FILE.read_text())

    logs.append({
        "time":time.time(),
        "event":event,
        "data":data
    })

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(
            logs,
            indent=2,
            ensure_ascii=False
        )
    )

    return logs[-1]
