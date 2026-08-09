from pathlib import Path
import sys

sys.path.insert(0,".ima")

from self_awareness.event_memory import record


def emit(event, data=None):
    try:
        record(event, data or {})
        return True
    except Exception as e:
        print("EVENT ERROR:", e)
        return False


if __name__=="__main__":
    emit(
        "event_bridge_online",
        {
            "status":"connected"
        }
    )

    print("EVENT BRIDGE ONLINE")
