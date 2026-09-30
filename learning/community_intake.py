"""Convert a public learning issue into a bounded, privacy-minimal learning queue entry."""
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
    number = issue.get("number")
    url = issue.get("html_url")
    record = {
        "schema": "IMA-COMMUNITY-LEARNING-1.0",
        "time": time.time(),
        "issue_number": number,
        "issue_url": url,
        "title": title,
        "status": "SUBMITTED",
        "next": ["TRIAGED", "GAP_MATCH", "SOURCE_CHECK", "RESEARCH", "TEST", "VERIFY", "TEACH"],
        "privacy_rule": "The issue body remains in GitHub. The shared queue stores only minimal routing metadata."
    }
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with QUEUE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record

if __name__ == "__main__":
    with open(os.environ["IMA_ISSUE_EVENT"], encoding="utf-8") as fh:
        payload = json.load(fh)
    print(json.dumps(intake(payload), ensure_ascii=False, indent=2))
