
from pathlib import Path
import json

FILE=Path("learning/world_memory.json")

def remember(question,data):

    if FILE.exists():
        mem=json.loads(FILE.read_text(encoding="utf8"))
    else:
        mem={}

    mem[question]=data

    FILE.write_text(
        json.dumps(mem,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

    return True
