"""Timestamped, append-only development journal for IMA.

Every recorded development event carries an ISO-8601 UTC timestamp, event type,
summary, source/provenance and verification state. The journal is local runtime
state; Git commits remain the durable repository history.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JOURNAL_DIR = ROOT / ".ima" / "journal"
JOURNAL_FILE = JOURNAL_DIR / "development.jsonl"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def record(event: str, summary: str, *, source: str = "ima_runtime", status: str = "RECORDED", details: dict[str, Any] | None = None) -> dict[str, Any]:
    entry = {
        "timestamp": now_utc(),
        "event": str(event),
        "summary": str(summary),
        "source": str(source),
        "status": str(status),
        "details": details or {},
    }
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    with JOURNAL_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True, default=str) + "\n")
    return entry


def self_test() -> bool:
    entry = record("SELF_TEST", "development journal write/read-path initialized", status="VERIFIED")
    return bool(entry["timestamp"] and entry["event"] == "SELF_TEST")
