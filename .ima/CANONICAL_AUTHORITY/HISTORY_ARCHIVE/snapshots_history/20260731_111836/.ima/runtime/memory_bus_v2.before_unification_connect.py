import json
import time
from pathlib import Path

LOG = Path(".ima/memory_log.jsonl")


def remember(event_type, data):
    entry = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }

    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def recall(keyword, limit=10):
    results = []

    if not LOG.exists():
        return results

    with LOG.open(encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)

                text = json.dumps(
                    item,
                    ensure_ascii=False
                )

                if keyword in text:
                    results.append(item)

            except Exception:
                pass

    return results[-limit:]


def status():
    return {
        "memory_bus_v2": True,
        "log_exists": LOG.exists()
    }
