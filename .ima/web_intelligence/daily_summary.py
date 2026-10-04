#!/usr/bin/env python3
"""Create a short, evidence-based daily IMA learning summary."""
from __future__ import annotations
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
STATE=ROOT/".ima/web_intelligence/state.json"
ADAPT=ROOT/".ima/web_intelligence/adaptation_state.json"
JOURNAL=ROOT/".ima/journal/development.jsonl"
DAILY=ROOT/".ima/journal/daily"
OUT=ROOT/"artifacts/web-intelligence/daily-summary.json"

def load(p, default):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return default

def today():
    return datetime.now(timezone.utc).astimezone().date().isoformat()

def run():
    d=today()
    state=load(STATE,{})
    adapt=load(ADAPT,{})
    events=[]
    if JOURNAL.exists():
        for line in JOURNAL.read_text(encoding="utf-8").splitlines():
            try:
                x=json.loads(line)
                if str(x.get("timestamp","")).startswith(d): events.append(x)
            except Exception: pass

    dimensions=adapt.get("dimensions",[])
    source_count=len(state.get("seen",{}))
    lessons=[]
    for x in dimensions[:6]:
        lessons.append(x)
    if events:
        lessons.append("validated changes and failures are part of learning")

    summary={
        "schema":"IMA-DAILY-SUMMARY-1.0",
        "date":d,
        "learning_count":len(lessons),
        "learned_today":lessons[:8],
        "discovery_seen_total":source_count,
        "journal_events_today":len(events),
        "status":"RECORDED"
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    DAILY.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    md="## IMA — סיכום למידה יומי\n\n"
    md+=f"**{d}**\n\n"
    md+=f"- למדה/בדקה: {len(lessons)} תחומי שיפור\n"
    md+=f"- אירועי פיתוח היום: {len(events)}\n"
    md+=f"- מקורות שנצברו במנוע הגילוי: {source_count}\n"
    if lessons:
        md+="\n**מה נלמד:**\n"+"\n".join(f"- {x}" for x in lessons[:5])+"\n"
    (DAILY/f"{d}.md").write_text(md,encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    run()
