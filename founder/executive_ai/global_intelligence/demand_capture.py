from __future__ import annotations
import hashlib, json, re, time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path("founder/data")
OUT = ROOT / "public_demand_signals.json"
CATEGORIES = {
    "real_estate": ["property", "real estate", "apartment", "house", "mortgage"],
    "vehicles": ["car", "vehicle", "fleet", "van", "truck"],
    "businesses_for_sale": ["business for sale", "company for sale", "acquisition"],
    "food": ["catering", "restaurant", "food supplier", "chef", "meal"],
    "travel": ["hotel", "travel", "tourism", "flight", "holiday"],
    "insurance": ["insurance", "coverage", "insurtech"],
    "b2b": ["supplier", "vendor", "procurement", "rfp", "wholesale"],
    "software": ["software", "saas", "api", "web development", "automation"],
    "equipment": ["machinery", "industrial equipment", "equipment rental"],
    "services": ["service", "consulting", "installation", "replacement", "agency"],
}
DEMAND = ("looking for", "need", "needed", "seeking", "wanted", "buyer", "supplier needed", "vendor needed", "rfp")

def fetch(url):
    req = Request(url, headers={"User-Agent": "IMA-Demand-Capture/1.0"})
    with urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")

def category(text):
    low = text.lower()
    for name, terms in CATEGORIES.items():
        if any(t in low for t in terms):
            return name
    return "general"

def capture(source, title, url, published=""):
    text = f"{title} {published}".strip()
    low = text.lower()
    if not any(t in low for t in DEMAND):
        return None
    cid = hashlib.sha256((source + url + title).encode()).hexdigest()[:20]
    return {
        "id": cid, "source": source, "title": title[:500], "url": url,
        "category": category(text), "public_demand": True,
        "opt_in_lead": False, "personal_data_collected": False,
        "consent_required_before_contact": True,
        "contactability": "unknown", "status": "DISCOVERED",
        "discovered_at": time.time()
    }

def scan_news():
    queries = [
        "property buyer OR tenant looking for", "car buyer looking for", "business for sale buyer",
        "catering needed OR restaurant supplier", "hotel booking travel buyer", "insurance needed",
        "supplier needed OR procurement RFP", "software needed OR web development looking for",
        "equipment buyer OR machinery needed", "service needed OR consulting looking for"
    ]
    rows = []
    for q in queries:
        url = "https://news.google.com/rss/search?q=" + quote(q) + "&hl=en-US&gl=US&ceid=US:en"
        try:
            root = ET.fromstring(fetch(url))
        except Exception:
            continue
        for item in root.findall("./channel/item")[:20]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            published = (item.findtext("pubDate") or "").strip()
            if title and link:
                row = capture("Google News RSS", title, link, published)
                if row: rows.append(row)
    return rows

def scan_all_sources():
    rows = scan_news()
    procurement_status = {}
    try:
        from founder.executive_ai.global_intelligence.procurement_capture import scan_all
        procurement, procurement_status = scan_all()
        rows.extend(procurement)
    except Exception as exc:
        procurement_status = {"status":"error","error":repr(exc)}
    return rows, procurement_status

def save(rows):
    ROOT.mkdir(parents=True, exist_ok=True)
    old = {}
    if OUT.exists():
        try: old = {r["id"]: r for r in json.loads(OUT.read_text())}
        except Exception: old = {}
    for row in rows: old[row["id"]] = row
    data = sorted(old.values(), key=lambda x: x.get("discovered_at", 0), reverse=True)[:5000]
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return data

def main():
    rows = scan_news()
    try:
        from founder.executive_ai.global_intelligence.procurement_capture import scan_all
        procurement, procurement_status = scan_all()
        rows.extend(procurement)
    except Exception as exc:
        procurement_status = {"status":"error","error":repr(exc)}
    data = save(rows)
    print(json.dumps({"new_signals": len(rows), "stored_signals": len(data), "file": str(OUT)}, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
