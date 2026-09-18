"""Public procurement demand adapters for IMA.
Only public published data is read; no submissions are performed.
"""
from __future__ import annotations
import hashlib, json, os, time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path("founder/data")
STATUS = ROOT / "procurement_source_status.json"

def fetch(url, headers=None, data=None):
    req = Request(url, headers={"User-Agent":"IMA-Procurement-Capture/1.0", **(headers or {})}, data=data)
    with urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")

def _signal(source, title, url, category="b2b", evidence=""):
    digest = hashlib.sha256((source+url+title).encode()).hexdigest()[:20]
    return {"id":digest,"source":source,"title":title[:500],"url":url,
            "category":category,"public_demand":True,"opt_in_lead":False,
            "personal_data_collected":False,"consent_required_before_contact":True,
            "contactability":"unknown","status":"DISCOVERED","evidence":evidence,
            "discovered_at":time.time()}

def scan_ted(limit=25):
    """Query TED's anonymous Search API for recently published notices."""
    since=time.strftime("%Y%m%d",time.gmtime(time.time()-14*86400))
    today=time.strftime("%Y%m%d",time.gmtime())
    body={"query":f"publication-date=({since} <> {today})","fields":["publication-number","notice-title","buyer-name","publication-date"],"page":1,"limit":limit,"scope":"ALL","checkQuerySyntax":False,"paginationMode":"PAGE_NUMBER"}
    url="https://api.ted.europa.eu/v3/notices/search"
    try:
        raw=fetch(url,headers={"Content-Type":"application/json","Accept":"application/json"},data=json.dumps(body).encode())
        payload=json.loads(raw); rows=[]
        for item in payload.get("notices",payload.get("results",[])):
            number=str(item.get("publication-number",item.get("publicationNumber","")))
            title=str(item.get("notice-title",item.get("noticeTitle","EU procurement notice")))
            date=str(item.get("publication-date",item.get("publicationDate","")))
            link="https://ted.europa.eu/en/notice/-/detail/"+number if number else "https://ted.europa.eu/"
            rows.append(_signal("TED Search API",title,link,"b2b",date))
        return rows,{"status":"ok","count":len(rows),"url":url}
    except Exception as exc:
        return [],{"status":"error","error":repr(exc),"url":url}

def scan_sam(limit=25):
    """Use SAM public API only when the user has supplied an API key in the environment."""
    key=os.environ.get("SAM_PUBLIC_API_KEY")
    if not key:
        return [], {"status":"auth_required","reason":"SAM_PUBLIC_API_KEY not configured","url":"https://sam.gov/opportunities"}
    url=("https://api.sam.gov/opportunities/v2/search?api_key="+quote(key)+"&limit="+str(limit)+"&postedFrom="+time.strftime("%m/%d/%Y",time.gmtime(time.time()-14*86400))+"&postedTo="+time.strftime("%m/%d/%Y",time.gmtime()))
    try:
        payload=json.loads(fetch(url)); rows=[]
        for item in payload.get("opportunitiesData",[]):
            title=item.get("title") or item.get("fullParentPathName") or "SAM.gov opportunity"
            notice=item.get("noticeId") or item.get("solicitationNumber") or ""
            link="https://sam.gov/opp/"+str(notice) if notice else "https://sam.gov/opportunities"
            rows.append(_signal("SAM.gov Contract Opportunities",title,link,"b2b",str(item.get("postedDate",""))))
        return rows, {"status":"ok","count":len(rows),"url":"https://sam.gov/opportunities"}
    except Exception as exc:
        return [], {"status":"error","error":repr(exc),"url":"https://sam.gov/opportunities"}

def scan_all():
    ted,ted_status=scan_ted(); sam,sam_status=scan_sam()
    status={"timestamp":time.time(),"sources":{"TED Open Data":ted_status,"SAM.gov Contract Opportunities":sam_status}}
    ROOT.mkdir(parents=True,exist_ok=True)
    STATUS.write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding="utf-8")
    return ted+sam,status
