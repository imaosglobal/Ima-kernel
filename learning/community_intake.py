"""Convert a public learning issue into a bounded, non-private learning queue entry."""
from __future__ import annotations
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "integrations" / "IMA_COMMUNITY_LEARNING_QUEUE.jsonl"

def _clean(value: str, limit: int = 240) -> str:
    value = re.sub(r"\s+", " ", str(value or "")).strip()
    return value[:limit]

def intake(event: dict) -> dict:
    issue = event.get("issue", event)
    title = _clean(issue.get("title"))
    body = _clean(issue.get("body"), 1200)
    number = issue.get("number")
    url = issue.get("html_url")
    record = {
        "schema": "IMA-COMMUNITY-LEARNING-1.0",
        "time": time.time(),
        "issue_number": number,
        "issue_url": url,
        "title": title,
        "summary": body,
        "status": "SUBMITTED",
        "next": ["TRIAGED", "GAP_MATCH", "SOURCE_CHECK", "RESEARCH", "TEST", "VERIFY", "TEACH"],
        "privacy_rule": "Do not copy secrets or confidential personal information into shared learning."
    }
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with QUEUE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record

if __name__ == "__main__":
    payload = json.load(open(os.environ["IMA_ISSUE_EVENT"], encoding="utf-8"))
    print(json.dumps(intake(payload), ensure_ascii=False, indent=2))
