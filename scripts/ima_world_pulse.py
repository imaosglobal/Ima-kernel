#!/usr/bin/env python3
"""IMA World Pulse: bounded public-source observation for global change.

Uses public, non-authenticated feeds. It records observations only; it does not
infer guilt, contact people, send aid, or execute interventions.
"""
from __future__ import annotations
import hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import requests

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/".ima/world_pulse/state.json"
ARTIFACT=ROOT/"artifacts/world-pulse/latest.json"
TIMEOUT=15
HEADERS={"User-Agent":"IMA-World-Pulse/1.0 (+https://github.com/imaosglobal/Ima-kernel)"}

QUERIES={
    "CONFLICT":"war OR conflict OR airstrike OR bombing",
    "PROTEST_OR_UPRISING":"protest OR uprising OR demonstration OR strike",
    "DISASTER":"earthquake OR flood OR wildfire OR hurricane OR cyclone OR tsunami",
    "HUMANITARIAN_DISPLACEMENT":"refugee OR displaced OR displacement",
    "PUBLIC_HEALTH":"outbreak OR epidemic OR pandemic OR health emergency",
    "RESOURCE_CRISIS":"famine OR drought OR food shortage OR water shortage",
    "POLITICAL_CHANGE":"election OR coup OR government OR president",
    "TECHNOLOGICAL_SHIFT":"artificial intelligence OR technology breakthrough",
    "SCIENTIFIC_SHIFT":"scientific discovery OR research breakthrough",
}

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]

def gdelt(kind, query):
    url="https://api.gdeltproject.org/api/v2/doc/doc?query="+quote(query)+"&mode=artlist&format=json&maxrecords=20&sort=datedesc"
    r=requests.get(url,headers=HEADERS,timeout=TIMEOUT)
    r.raise_for_status()
    rows=r.json().get("articles",[])
    out=[]
    for row in rows:
        title=str(row.get("title") or "").strip()
        link=str(row.get("url") or "").strip()
        if not title or not link.startswith(("http://","https://")):
            continue
        out.append({
            "id":digest(link),
            "event_type":kind,
            "title":title[:300],
            "source_url":link,
            "source_name":"GDELT",
            "observed_at":now(),
            "published_at":row.get("seendate"),
            "domain":row.get("domain"),
            "evidence_status":"REPORTED_PUBLIC_SOURCE",
            "confidence":"UNKNOWN",
        })
    return out

def reliefweb():
    url="https://api.reliefweb.int/v2/disasters?appname=imaosglobal-ima&limit=30&profile=full&preset=latest"
    r=requests.get(url,headers=HEADERS,timeout=TIMEOUT)
    r.raise_for_status()
    out=[]
    for row in r.json().get("data",[]):
        fields=row.get("fields",{})
        name=str(fields.get("name") or "").strip()
        if not name:
            continue
        url_value=str(fields.get("url") or "https://reliefweb.int/").strip()
        out.append({
            "id":"reliefweb-"+str(row.get("id")),
            "event_type":"DISASTER",
            "title":name[:300],
            "source_url":url_value,
            "source_name":"ReliefWeb",
            "observed_at":now(),
            "published_at":fields.get("date",{}).get("created") if isinstance(fields.get("date"),dict) else None,
            "country":fields.get("country"),
            "evidence_status":"REPORTED_PUBLIC_HUMANITARIAN_SOURCE",
            "confidence":"UNKNOWN",
        })
    return out

def run():
    items=[]; errors=[]
    for kind,q in QUERIES.items():
        try: items.extend(gdelt(kind,q))
        except Exception as exc: errors.append({"source":"GDELT","kind":kind,"error":type(exc).__name__})
    try: items.extend(reliefweb())
    except Exception as exc: errors.append({"source":"ReliefWeb","error":type(exc).__name__})
    unique={x["id"]:x for x in items}
    items=list(unique.values())
    record={
        "schema":"IMA-WORLD-PULSE-1.0",
        "timestamp":now(),
        "status":"OBSERVED_WITH_PUBLIC_SOURCES",
        "coverage":"BOUNDED_NOT_EXHAUSTIVE",
        "items":items[:250],
        "errors":errors,
        "principles":[
            "reported_source_is_not_verified_fact",
            "classification_is_not_guilt",
            "no_collective_blame",
            "nonviolence_default",
            "humanitarian_needs_before_political_judgment",
            "human_authorization_required_for_external_action",
        ],
    }
    STATE.parent.mkdir(parents=True,exist_ok=True)
    ARTIFACT.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    ARTIFACT.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":record["status"],"observed":len(items),"errors":len(errors),
        "coverage":record["coverage"],"artifact":str(ARTIFACT.relative_to(ROOT))
    },ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(run())
