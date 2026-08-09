from pathlib import Path
import json
import time

REGISTRY=Path(".ima/llm_registry.json")

def save(models):
    data={
        "time":time.time(),
        "models":models
    }

    REGISTRY.write_text(
        json.dumps(data,indent=2,ensure_ascii=False),
        encoding="utf-8"
    )

    return data


def load():
    if not REGISTRY.exists():
        return {"models":[]}

    return json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )
