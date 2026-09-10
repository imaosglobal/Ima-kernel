import json
import time
from pathlib import Path

from .router import select_provider

REGISTRY = Path(".ima/llm_selection.json")


def select():
    provider = select_provider()

    selected = {
        "time": time.time(),
        "selected": provider,
        "provider": provider.get("provider"),
    }

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
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
    try:
        if REGISTRY.exists():
            data = json.loads(
                REGISTRY.read_text(encoding="utf-8")
            )

            provider = data.get("provider")
            if provider:
                return data
    except Exception:
        pass

    return select()
