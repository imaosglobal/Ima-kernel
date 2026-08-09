import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent

MEMORY_TARGET = Path.home() / ".ima/software_learning.jsonl"

def load_brain():
    from software_brain import analyze
    from learning_graph import understand

    return {
        "software": analyze(),
        "graph": understand()
    }


def save_to_ima(data):
    MEMORY_TARGET.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    record = {
        "time": datetime.now().isoformat(),
        "source": "software_intelligence",
        "data": data
    }

    with open(MEMORY_TARGET,"a",encoding="utf-8") as f:
        f.write(
            json.dumps(record,ensure_ascii=False)
            + "\n"
        )


if __name__ == "__main__":
    knowledge = load_brain()
    save_to_ima(knowledge)

    print("IMA MEMORY UPDATED")
    print(MEMORY_TARGET)
