"""IMA Deal Hunter: discovery, matching, consent-gated referral workflow and payout ledger."""
from __future__ import annotations
import hashlib, json, re, sys, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from founder.executive_ai.global_intelligence.marketplace_adapters import route_for, all_marketplaces
from founder.executive_ai.global_intelligence.commerce_pipeline import create as create_pipeline

ROOT = Path("founder/data")
DATA = ROOT / "deal_hunter_opportunities.json"
LEADS = ROOT / "deal_hunter_leads.json"
REFERRALS = ROOT / "deal_hunter_referrals.json"
PAYOUTS = ROOT / "deal_hunter_payouts.json"
ACTIONS = ROOT / "deal_hunter_actions.json"

CATEGORIES = {
    "real_estate": ["real estate","property","mortgage","housing","apartment","house"],
    "vehicles": ["car","vehicle","fleet","auto","van","truck"],
    "insurance": ["insurance","insurtech","cover","coverage"],
    "travel": ["travel","hotel","tourism","flight","holiday","vacation"],
    "b2b": ["b2b","business","supplier","vendor","procurement","rfp"],
    "software": ["software","saas","api","automation","ai","web design","development"],
    "equipment": ["equipment","machinery","industrial","equipment rental"],
    "services": ["service","agency","consulting","installation","replacement"],
    "food": ["food","restaurant","catering","chef","meal"],
}
DEMAND_TERMS = ("looking for","need","wanted","seeking","request for proposal","rfp","buyer","purchase","supplier needed","vendor needed")
MONEY_TERMS = ("referral fee","referral commission","commission","payout","pay per lead","per lead","paid","fee","bounty")

class _TextParser(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data):
        if data.strip(): self.parts.append(data.strip())

def fetch(url, timeout=15):
    req=Request(url,headers={"User-Agent":"IMA-Deal-Hunter/2.0"})
    with urlopen(req,timeout=timeout) as r: return r.read().decode("utf-8",errors="replace")

def clean_html(text):
    p=_TextParser(); p.feed(text)
    return re.sub(r"\s+"," "," ".join(p.parts)).strip()

def category_for(text):
    low=text.lower()
    for category,terms in CATEGORIES.items():
        if any(t in low for t in terms): return category
    return "general"

def score(text):
    low=text.lower(); points=0; reasons=[]
    demand=sum(t in low for t in DEMAND_TERMS); money=sum(t in low for t in MONEY_TERMS)
    if demand: points+=min(35,demand*10); reasons.append("explicit demand signal")
    if money: points+=min(40,money*10); reasons.append("monetization signal")
    if any(x in low for x in ("global","worldwide","international")): points+=10; reasons.append("global coverage")
    if any(x in low for x in ("free","no cost","no upfront")): points+=10; reasons.append("zero-upfront signal")
    return min(100,points),reasons

def _deal(source,title,url,text,payout=None,currency=None,payout_model=None):
    value=f"{title} {text}"; confidence,reasons=score(value)
    digest=hashlib.sha256((source+url+title).encode()).hexdigest()[:20]
    return {"id":digest,"source":source,"title":title[:300],"url":url,"category":category_for(value),
            "signal":text[:2000],"confidence":confidence,"evidence":reasons,
            "verification_status":"public-source-unverified","consent_required":True,
            "discovered_at":time.time(),"payout_amount":payout,"payout_currency":currency,
            "payout_model":payout_model,"next_action":"verify_terms_then_request_consent_before_contact"}

def scan_referr():
    url="https://www.referr.co.uk/"
    try: raw=fetch(url)
    except Exception as exc: return [{"source":"Referr","error":str(exc),"url":url}]
    text=clean_html(raw); results=[]
    # Accept only explicit lead-request language; ignore FAQ/schema marketing text.
    patterns=re.findall(r"([A-Z][A-Za-z]{1,40})\s+is looking for\s+([^|.]{3,140})\s+leads",text,re.I)
    for name, need in patterns[:100]:
        title=f"{name} is looking for {need.strip()} leads"
        results.append(_deal("Referr",title,url,title,payout_model="per_lead"))
    return results

def scan_public_rss():
    queries=[
      ("real_estate","real estate referral fee OR commission"),("vehicles","car buyer lead referral commission"),
      ("insurance","insurance referral fee lead"),("travel","hotel travel referral commission lead"),
      ("b2b","supplier needed referral fee OR commission"),("software","web development looking for referral fee"),
      ("equipment","equipment buyer referral commission"),("services","service needed referral fee"),("food","catering needed referral commission")]
    out=[]
    for category,q in queries:
        url="https://news.google.com/rss/search?q="+quote(q)+"&hl=en-US&gl=US&ceid=US:en"
        try: root=ET.fromstring(fetch(url)); items=root.findall("./channel/item")
        except Exception: continue
        for item in items[:12]:
            title=(item.findtext("title") or "").strip(); link=(item.findtext("link") or "").strip(); desc=clean_html(item.findtext("description") or "")
            if not title or not link: continue
            d=_deal("Google News RSS",title,link,desc); d["category"]=category; out.append(d)
    return out
def _load(path):
    try: return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except Exception: return []

def _save(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")

def load_saved(): return _load(DATA)

def save_unique(records):
    old={r.get("id"):r for r in load_saved() if r.get("id")}
    for r in records:
        if r.get("id"): old[r["id"]]=r
    rows=sorted(old.values(),key=lambda x:x.get("confidence",0),reverse=True)[:2000]
    _save(DATA,rows); return rows

def add_lead(lead):
    """Store only a lead whose owner has explicitly opted in to referral sharing."""
    required=("lead_id","category","need","consent","consent_at")
    if not all(k in lead for k in required) or lead.get("consent") is not True:
        raise ValueError("explicit opt-in consent is required")
    lead={**lead,"created_at":lead.get("created_at",time.time()),"status":"qualified"}
    rows=_load(LEADS); rows=[r for r in rows if r.get("lead_id")!=lead["lead_id"]]; rows.append(lead)
    _save(LEADS,rows); return lead

def match_leads():
    leads=_load(LEADS); deals=load_saved(); matches=[]
    for lead in leads:
        if lead.get("consent") is not True: continue
        lt=(str(lead.get("need",""))+" "+str(lead.get("category",""))).lower()
        for deal in deals:
            dt=(str(deal.get("title",""))+" "+str(deal.get("signal",""))+" "+str(deal.get("category",""))).lower()
            category=lead.get("category")
            score=0
            if category and category==deal.get("category"): score+=50
            words={w for w in re.findall(r"[\w\u0590-\u05ff]{3,}",lt, re.UNICODE)
                   if w not in {"looking","need","want","אני","צריך","מחפש","מחפשת"}}
            score+=min(35,sum(w in dt for w in words)*7)
            if deal.get("payout_amount"): score+=10
            if deal.get("verification_status","").startswith("public-listing"): score+=5
            if score>=45: matches.append({"lead_id":lead["lead_id"],"deal_id":deal.get("id"),"score":min(100,score),"created_at":time.time()})
    matches.sort(key=lambda x:x["score"],reverse=True); _save(REFERRALS,matches); return matches

def build_actions(matches):
    actions=[]
    deals={d.get("id"):d for d in load_saved()}
    leads={l.get("lead_id"):l for l in _load(LEADS)}
    for m in matches[:100]:
        d=deals.get(m.get("deal_id")); l=leads.get(m.get("lead_id"))
        if not d or not l: continue
        routes=route_for(d)
        pipelines=[]
        for route in routes:
            p=create_pipeline(d,route["name"])
            if p: pipelines.append(p["pipeline_id"])
        actions.append({"action_id":hashlib.sha256((m["lead_id"]+str(m["deal_id"])).encode()).hexdigest()[:16],
          "type":"submit_referral","lead_id":m["lead_id"],"deal_id":m["deal_id"],"score":m["score"],
          "target_url":d.get("url"),"status":"ready_for_authorized_submission",
          "requires_user_or_platform_auth":True,"consent_verified":l.get("consent") is True,
          "marketplace_routes":routes,"created_at":time.time()})
    _save(ACTIONS,actions); return actions

def record_referral(referral):
    allowed={"qualified","submitted","accepted","converted","rejected","paid"}
    if referral.get("status") not in allowed: raise ValueError("invalid referral status")
    rows=_load(REFERRALS); rows.append({**referral,"updated_at":time.time()}); _save(REFERRALS,rows); return referral

def record_payout(payout):
    if not payout.get("referral_id") or payout.get("amount") is None: raise ValueError("referral_id and amount required")
    rows=_load(PAYOUTS); rows.append({**payout,"recorded_at":time.time()}); _save(PAYOUTS,rows); return payout
def run_once():
    discovered=scan_referr()+scan_public_rss()
    saved=save_unique(discovered)
    matches=match_leads(); actions=build_actions(matches)
    return {"discovered":len(discovered),"stored":len(saved),"matched":len(matches),"actions":len(actions),"top":saved[:20]}

def status():
    return {"deals":len(load_saved()),"opt_in_leads":len(_load(LEADS)),
            "matches":len(_load(REFERRALS)),"actions":len(_load(ACTIONS)),"payout_records":len(_load(PAYOUTS))}

def main():
    if len(sys.argv)>1 and sys.argv[1]=="marketplaces": print(json.dumps(all_marketplaces(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="connectors":
        from founder.executive_ai.global_intelligence.connector_dispatcher import readiness
        print(json.dumps(readiness(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="pipeline":
        from founder.executive_ai.global_intelligence.commerce_pipeline import summary
        print(json.dumps(summary(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="status": print(json.dumps(status(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="demand":
        from founder.executive_ai.global_intelligence.demand_capture import main as demand_main
        demand_main(); return
    if len(sys.argv)>1 and sys.argv[1]=="global":
        from founder.executive_ai.global_intelligence.global_opportunity_graph import build
        print(json.dumps(build(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="global-status":
        from founder.executive_ai.global_intelligence.global_opportunity_graph import summary
        print(json.dumps(summary(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="sources":
        from founder.executive_ai.global_intelligence.global_source_registry import all_sources
        print(json.dumps(all_sources(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="autonomy":
        from founder.executive_ai.global_intelligence.autonomy_orchestrator import cycle
        print(json.dumps(cycle(),ensure_ascii=False,indent=2)); return
    if len(sys.argv)>1 and sys.argv[1]=="match": print(json.dumps({"matches":match_leads()},ensure_ascii=False,indent=2)); return
    print(json.dumps(run_once(),ensure_ascii=False,indent=2))

if __name__=="__main__": main()
