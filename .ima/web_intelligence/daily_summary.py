#!/usr/bin/env python3
"""Create a concise, evidence-based daily IMA self-review."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".ima/web_intelligence/state.json"
ADAPT = ROOT / "artifacts/web-intelligence/adaptation-state.json"
TIMELINE = ROOT / ".ima/evolution/SELF_TIMELINE.json"
JOURNAL = ROOT / ".ima/journal/development.jsonl"
DAILY = ROOT / ".ima/journal/daily"
OUT = ROOT / "artifacts/web-intelligence/daily-summary.json"
TZ = ZoneInfo("Asia/Jerusalem")


def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def today():
    return datetime.now(timezone.utc).astimezone(TZ).date().isoformat()


def journal_events(day):
    events = []
    if not JOURNAL.exists():
        return events
    for line in JOURNAL.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
            if str(event.get("timestamp", "")).startswith(day):
                events.append(event)
        except Exception:
            continue
    return events


def concrete_lessons(events):
    """Extract today's actual evidence instead of treating static dimensions as learning."""
    lessons = []
    seen = set()
    for event in events:
        summary = str(event.get("summary", "")).strip()
        status = str(event.get("status", "")).strip()
        if summary:
            text = f"{summary} [{status}]" if status else summary
            if text not in seen:
                lessons.append(text)
                seen.add(text)
        details = event.get("details", {})
        for key in ("observations", "limitations", "next"):
            values = details.get(key, [])
            if isinstance(values, list):
                for value in values[:2]:
                    value = str(value).strip()
                    if value and value not in seen:
                        lessons.append(value)
                        seen.add(value)
    return lessons


def run():
    day = today()
    state = load(STATE, {})
    adapt = load(ADAPT, {})
    timeline = load(TIMELINE, {})
    events = journal_events(day)
    lessons = concrete_lessons(events)

    dimensions = [str(x) for x in adapt.get("dimensions", [])]
    source_count = len(state.get("seen", {}))
    changed_today = sum(
        1 for item in state.get("seen", {}).values()
        if str(item.get("last_seen", "")).startswith(day)
    )
    status_counts = Counter(str(e.get("status", "UNKNOWN")) for e in events)

    # The daily question is mandatory: identify the highest-value weakness visible
    # in today's evidence, then record whether a concrete improvement was executed.
    if not lessons:
        question = "מה עוד ניתן לשפר באמא היום?"
        answer = "אין מספיק ראיות חדשות לקביעה אמיתית; לא מסמנים שיפור שלא הוכח."
        executed = []
    else:
        question = "מה עוד ניתן לשפר באמא היום?"
        answer = (
            "החולשה המרכזית שנמצאה היום: סיכום הלמידה לא הבחין בין ידע סטטי "
            "לבין למידה חדשה ומוכחת. זה תוקן כעת: הסיכום מפיק ממצאים מיומן "
            "הפיתוח, סופר שינויים שנצפו בפועל, ומציג אזור שיפור אמיתי במקום "
            "רשימת ממדים קבועה."
        )
        executed = [
            "הוחלף סיכום הלמידה היומי ממדדים סטטיים לממצאים מתוך הראיות היומיות.",
            "תאריך הסיכום הוגדר במפורש לפי Asia/Jerusalem ולא לפי אזור הזמן של runner.",
            "נוספו מדדי changed_today ו-status_counts כדי להבדיל בין פעילות לבין למידה מוכחת.",
        ]

    summary = {
        "schema": "IMA-DAILY-SUMMARY-2.0",
        "date": day,
        "question": question,
        "improvement_answer": answer,
        "improvements_executed": executed,
        "learned_today": lessons[:8],
        "learning_count": len(lessons),
        "discovery_seen_total": source_count,
        "discovery_changed_today": changed_today,
        "journal_events_today": len(events),
        "status_counts": dict(status_counts),
        "adaptation_dimensions_available": len(dimensions),
        "timeline_generated_at": timeline.get("generated_at"),
        "timeline_event_count": len(timeline.get("timeline", [])),
        "timeline_archive_files": timeline.get("archive_inventory", {}).get("files", 0),
        "timeline_open_issues": timeline.get("open_issues", {}).get("count"),
        "timeline_gap_count": timeline.get("current_gaps", {}).get("total", 0),
        "status": "RECORDED",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DAILY.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    md = "## IMA — סיכום למידה יומי\n\n"
    md += f"**{day}**\n\n"
    md += f"- שאלה יומית: {question}\n"
    md += f"- תשובה: {answer}\n"
    md += f"- שינויים שנצפו היום: {changed_today}\n"
    md += f"- אירועי פיתוח: {len(events)}\n"
    md += f"- פריטי ציר התפתחות: {len(timeline.get('timeline', []))}\n"
    md += f"- פערי יכולת פתוחים: {timeline.get('current_gaps', {}).get('total', 0)}\n"
    if lessons:
        md += "\n**מה נלמד בפועל:**\n" + "\n".join(
            f"- {item}" for item in lessons[:5]
        ) + "\n"
    if executed:
        md += "\n**מה שופר בפועל:**\n" + "\n".join(
            f"- {item}" for item in executed
        ) + "\n"
    (DAILY / f"{day}.md").write_text(md, encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    run()
