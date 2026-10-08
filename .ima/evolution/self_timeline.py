#!/usr/bin/env python3
"""Build IMA's chronological self-evolution ledger from durable project evidence."""
from __future__ import annotations
import json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[2]
SEED=ROOT/".ima/evolution/HISTORY_SEED.json"
JOURNAL=ROOT/".ima/journal/development.jsonl"
DAILY=ROOT/".ima/journal/daily"
GAPS=ROOT/"integrations/IMA_CAPABILITY_GAPS.json"
OUT=ROOT/".ima/evolution/SELF_TIMELINE.json"
DOC=ROOT/"docs/IMA_SELF_EVOLUTION_TIMELINE.md"

def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def git_history(limit=250):
    try:
        raw=subprocess.check_output(["git","log","--reverse",f"--max-count={limit}","--format=%H%x09%cI%x09%s"],cwd=ROOT,text=True)
    except Exception:
        return []
    out=[]
    for line in raw.splitlines():
        parts=line.split("\t",2)
        if len(parts)==3:
            out.append({"commit":parts[0],"timestamp":parts[1],"event":"commit","summary":parts[2],"source":"git"})
    return out

def journal_history():
    out=[]
    if not JOURNAL.exists():
        return out
    for line in JOURNAL.read_text(encoding="utf-8").splitlines():
        try:
            e=json.loads(line)
            out.append({"timestamp":e.get("timestamp"),"event":e.get("event"),"summary":e.get("summary"),"status":e.get("status"),"source":e.get("source","development.jsonl")})
        except Exception:
            pass
    return out

def daily_history():
    out=[]
    for p in sorted(DAILY.glob("*.md")):
        out.append({"date":p.stem,"event":"daily_summary","summary":p.read_text(encoding="utf-8")[:1000],"source":str(p)})
    return out

def archive_inventory():
    try:
        raw=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True)
    except Exception:
        return {"files":0,"families":{}}
    paths=[p for p in raw.splitlines() if any(x in p.lower() for x in ("_archive","_graveyard","/archive/","backup","backups"))]
    families={}
    for p in paths:
        low=p.lower()
        family=("memory" if "memory" in low else
                "learning" if "learn" in low else
                "evolution" if "evol" in low else
                "guardian" if "guardian" in low else
                "knowledge" if "knowledge" in low else
                "security" if "security" in low or "auth" in low else
                "runtime" if "runtime" in low or "kernel" in low else "other")
        families[family]=families.get(family,0)+1
    return {"files":len(paths),"families":families}

def open_issues():
    token=os.getenv("GITHUB_TOKEN")
    if not token:
        return {"status":"UNAVAILABLE","count":None,"items":[]}
    url=os.getenv("GITHUB_API_URL","https://api.github.com")+"/repos/imaosglobal/Ima-kernel/issues?state=open&per_page=100"
    try:
        req=Request(url,headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json"})
        data=json.load(urlopen(req,timeout=10))
        items=[{"number":x["number"],"title":x["title"],"url":x["html_url"]} for x in data if "pull_request" not in x]
        return {"status":"VERIFIED","count":len(items),"items":items}
    except Exception as exc:
        return {"status":"ERROR","count":None,"items":[],"error":type(exc).__name__}

def build():
    seed=read_json(SEED,{"entries":[]})
    gaps=read_json(GAPS,{"gaps":[]}).get("gaps",[])
    journal=journal_history()
    daily=daily_history()
    events=seed.get("entries",[])+git_history()+journal+daily
    events.sort(key=lambda x:str(x.get("timestamp") or x.get("date") or ""))
    timeline={
        "schema":"IMA-SELF-TIMELINE-1.0",
        "generated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "principle":"remember without becoming trapped by memory; preserve history while continuously reassessing it",
        "sources":{"conversation_history_seed":len(seed.get("entries",[])),"git_commits":len([x for x in events if x.get("source")=="git"]),"development_journal":len(journal),"daily_summaries":len(daily)},
        "archive_inventory":archive_inventory(),
        "open_issues":open_issues(),
        "current_gaps":{"total":len(gaps),"by_state":{},"items":gaps},
        "timeline":events[-500:]
    }
    for g in gaps:
        s=str(g.get("state","unknown"))
        timeline["current_gaps"]["by_state"][s]=timeline["current_gaps"]["by_state"].get(s,0)+1
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# IMA — ציר ההתפתחות העצמית","","המסמך נבנה מחדש בכל מחזור מתוך Git, יומן הפיתוח, היומנים היומיים, עוגני ההיסטוריה וארכיון הקוד.","","## מצב נוכחי"]
    lines += [f"- נוצר: {timeline['generated_at']}",f"- פערי יכולת פתוחים: {len(gaps)}",f"- פריטי ארכיון/גיבוי שנסרקו: {timeline['archive_inventory']['files']}",f"- Issues פתוחים שנאספו: {timeline['open_issues']['count'] if timeline['open_issues']['count'] is not None else 'UNAVAILABLE'}",""]
    lines += ["## עקרון הציר","1. מה קרה בפועל?","2. מה השתפר?","3. מה עדיין לא הוכח או לא הושלם?","4. מה השתנה בעולם?","5. מה ניתן לחדש עכשיו?","6. מה צריך להיבדק מחדש מחר?",""]
    lines += ["## נקודות ציון אחרונות"]
    for e in timeline["timeline"][-30:]:
        when=e.get("timestamp") or e.get("date") or "unknown"
        lines.append(f"- {when} — {e.get('event','event')} — {str(e.get('summary','')).splitlines()[0][:220]}")
    lines += ["","## פערי יכולת",""]
    for g in gaps:
        lines.append(f"- {g.get('id')} — {g.get('state')} / {g.get('priority')} — {g.get('capability')}")
    lines += ["","## כלל יומי","הציר נבנה מחדש בכל יום. שינוי חדש אינו נחשב שיפור עד שיש לו מקור, שינוי ברור, בדיקה וראיית אימות מתאימה. כשל נשמר כחלק מההיסטוריה ולא נעלם."]
    DOC.parent.mkdir(parents=True,exist_ok=True)
    DOC.write_text("\n".join(lines)+"\n",encoding="utf-8")
    return timeline

if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False))
