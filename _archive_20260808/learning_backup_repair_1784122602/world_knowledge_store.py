
from pathlib import Path
import json

FILE=Path("learning/world_knowledge.json")

def save(question,data):
    if FILE.exists():
        store=json.loads(FILE.read_text(encoding="utf8"))
    else:
        store={}

    store[question]=data

    FILE.write_text(
        json.dumps(store,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

    return store[question]
