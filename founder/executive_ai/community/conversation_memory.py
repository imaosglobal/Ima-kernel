from pathlib import Path
import json
import time

from founder.executive_ai.memory.memory_store import save_memory as _canonical_save_memory

FILE = Path("founder/data/conversation_memory.json")


def save_message(user, message):
    entry = {
        "user": user,
        "message": message,
        "timestamp": time.time(),
    }

    FILE.parent.mkdir(parents=True, exist_ok=True)

    data = []
    if FILE.exists():
        try:
            loaded = json.loads(FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                data = loaded
        except Exception:
            data = []

    data.append(entry)
    FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Canonical operational memory.
    _canonical_save_memory(
        key="conversation",
        value=entry,
        category="conversation",
        importance=70,
    )

    return entry
