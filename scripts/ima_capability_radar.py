#!/usr/bin/env python3
"""Fetch configured public RSS/Atom metadata into an append-only IMA discovery log."""
import datetime as dt, hashlib, json, pathlib, urllib.request, xml.etree.ElementTree as ET
ROOT=pathlib.Path(".ima/intelligence_radar")
sources=json.loads((ROOT/"sources.json").read_text(encoding="utf-8"))["sources"]
log=ROOT/"observations.jsonl"
seen=set()
if log.exists():
    for line in log.read_text(encoding="utf-8").splitlines():
        try: seen.add(json.loads(line).get("id"))
        except Exception: pass
now=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
counts={"scanned":0,"new":0,"failed":0,"unchanged":0}
records=[]
for source in sources:
    try:
        req=urllib.request.Request(source["url"],headers={"User-Agent":"IMA-Capability-Radar/1.0 (+public metadata discovery)"})
        with urllib.request.urlopen(req,timeout=25) as response:
            payload=response.read(2_500_000)
        root=ET.fromstring(payload)
        entries=[]
        for node in root.iter():
            tag=node.tag.rsplit("}",1)[-1].lower()
            if tag in ("item","entry"):
                def child(*names):
                    for c in node:
                        if c.tag.rsplit("}",1)[-1].lower() in names:
                            if c.text and c.text.strip(): return c.text.strip()
                            href=c.attrib.get("href")
                            if href: return href
                    return ""
                title=child("title")
                link=child("link","id")
                published=child("published","updated","pubdate","date")
                summary=child("summary","description","content")
                if title and link:
                    entries.append((title,link,published,summary[:1200]))
        counts["scanned"]+=1
        for title,url,published,summary in entries:
            key=hashlib.sha256((url.strip()+"\n"+title.strip().lower()).encode()).hexdigest()
            if key in seen: counts["unchanged"]+=1; continue
            rec={"timestamp":now,"id":key,"event":"AI_CAPABILITY_DISCOVERY","status":"DISCOVERED_UNREVIEWED","source":source["name"],"source_url":source["url"],"title":title,"url":url,"published":published or None,"summary":summary,"classification":"UNCLASSIFIED","decision":"NOT_EVALUATED","limitations":"Feed metadata only; announcement, availability, suitability, and capability are not independently verified."}
            records.append(rec); seen.add(key); counts["new"]+=1
    except Exception as exc:
        counts["failed"]+=1
        records.append({"timestamp":now,"event":"RADAR_SOURCE_FAILURE","status":"GAP_RECORDED","source":source["name"],"source_url":source["url"],"error_type":type(exc).__name__,"error":str(exc)[:400],"meaning":"Source could not be scanned; no conclusion about whether updates exist."})
ROOT.mkdir(parents=True,exist_ok=True)
with log.open("a",encoding="utf-8") as f:
    for rec in records: f.write(json.dumps(rec,ensure_ascii=False,separators=(",",":"))+"\n")
summary={"timestamp":now,"counts":counts,"new_records":counts["new"],"source_failures":counts["failed"],"coverage":"Configured watchlist only; not exhaustive."}
(ROOT/"latest_scan.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
