import json
from pathlib import Path
from datetime import datetime
import time
try:
    from founder.executive_ai.memory.autobiography_bus import ima_event
except ImportError:
    def ima_event(*args, **kwargs):
        return None


FILE = Path("founder/data/ima_memory.json")


def save_memory(
    key,
    value,
    category="general",
    importance=0
):
    entry = {
        "timestamp": time.time(),
        "datetime": datetime.now().isoformat(),
        "key": key,
        "value": value,
        "category": category,
        "importance": importance
    }

    data = []

    if FILE.exists():
        data = json.loads(
            FILE.read_text(encoding="utf8")
        )

    data.append(entry)

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    # CANONICAL IMA AUTOBIOGRAPHY
    # Record provenance only after the operational memory
    # persistence has completed successfully.
    try:
        ima_event(
            "memory_change",
            {
                "key": key,
                "value": value,
                "category": category,
                "importance": importance,
            },
            source="memory_store",
        )
    except Exception:
        pass

    return entry


def get_memories():

    if FILE.exists():
        return json.loads(
            FILE.read_text(encoding="utf8")
        )

    return []


def find_memory(key):

    return [
        x for x in get_memories()
        if x.get("key") == key
    ]


def save_action(action):

    return save_memory(
        key="action",
        value=action,
        category="executive_action",
        importance=50
    )


def load_memory():

    return get_memories()


def query_memory(
    query=None,
    category=None
):

    results = get_memories()

    if query is not None:
        results = [
            x for x in results
            if query in str(x.get("value", ""))
            or query in str(x.get("key", ""))
        ]

    if category is not None:
        results = [
            x for x in results
            if x.get("category") == category
        ]

    return results
