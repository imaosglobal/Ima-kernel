from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"

if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

try:
    from stream import emit
except Exception:
    emit = None


def bridge_event(event_type, **data):
    """
    event_bridge -> runtime.stream.emit
    """
    if emit:
        return emit(event_type, **data)

    return {
        "status": "stream_unavailable",
        "event": event_type,
        "data": data
    }


def health():
    return {
        "bridge": "stream_bridge",
        "connected": emit is not None
    }
