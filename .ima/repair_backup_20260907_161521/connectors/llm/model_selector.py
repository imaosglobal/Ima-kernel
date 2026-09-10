from pathlib import Path
import json
import time

from .discovery_engine import discover
from .capability_test import rank

REGISTRY=Path(".ima/llm_selection.json")


def select():

    data=discover()

    models=[
        m["name"]
        for m in data.get("local_models",[])
    ]

    if not models:
        return {
            "model":"none",
            "status":"no_models"
        }

    ranked=rank(models)

    selected={
        "time":time.time(),
        "selected":ranked[0],
        "ranking":ranked
    }

    REGISTRY.write_text(
        json.dumps(
            selected,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return selected


def current():

    if REGISTRY.exists():
        return json.loads(
            REGISTRY.read_text(encoding="utf-8")
        )

    return select()
