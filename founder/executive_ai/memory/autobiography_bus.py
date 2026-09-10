"""
IMA Autobiography Event Bus

Compatibility layer for the canonical memory system.

Provides:
    ima_event(...)
    user_message(...)

The bus is intentionally lightweight and must never prevent
the core memory system from operating.
"""

import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

DATA_DIR = ROOT / "founder" / "data"
EVENT_FILE = DATA_DIR / "autobiography_events.jsonl"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def _write_event(event):
    try:
        with EVENT_FILE.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    event,
                    ensure_ascii=False,
                    default=str,
                )
                + "\n"
            )
        return event
    except Exception:
        # Memory/event logging must never break the main runtime.
        return event


def ima_event(
    event_type,
    data=None,
    importance=50,
    *args,
    **kwargs,
):
    """
    Record an IMA system event.

    Supports the calling convention already used by event_bus.py
    and other legacy callers.
    """

    event = {
        "timestamp": time.time(),
        "source": "IMA",
        "event_type": str(event_type),
        "importance": importance,
        "data": data if data is not None else {},
    }

    if args:
        event["args"] = list(args)

    if kwargs:
        event["kwargs"] = kwargs

    return _write_event(event)


def user_message(
    message,
    user_id=None,
    *args,
    **kwargs,
):
    """
    Record a user message in the autobiography/event stream.
    """

    return ima_event(
        "user_message",
        {
            "message": message,
            "user_id": user_id,
            **kwargs,
        },
        importance=70,
        *args,
    )


__all__ = [
    "ima_event",
    "user_message",
]
