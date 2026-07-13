
import json
from pathlib import Path

FILE=Path("learning/world_memory.json")

def store(topic,data):
    memory={}

    if FILE.exists():
        memory=json.loads(FILE.read_text())

    memory.setdefault(topic,[]).append(data)

    FILE.write_text(
        json.dumps(memory,ensure_ascii=False,indent=2)
    )

    return memory
