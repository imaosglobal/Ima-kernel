
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List

FILE = Path("founder/data/economic_memory.json")


def _load() -> List[Dict[str, Any]]:
    if not FILE.exists():
        return []
    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_economic_event(event: Dict[str, Any]) -> Dict[str, Any]:
    FILE.parent.mkdir(parents=True, exist_ok=True)

    records = _load()

    record = {
        "time": time.time(),
        **event,
    }

    records.append(record)

    FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return record


def get_economic_memory() -> List[Dict[str, Any]]:
    return _load()
