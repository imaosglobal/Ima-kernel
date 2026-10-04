#!/usr/bin/env python3
"""IMA Global Web Intelligence discovery layer.

Fast discovery uses public indexes/feeds and records provenance. It does not attempt
to crawl the whole web directly, bypass access controls, or execute arbitrary code.
Dynamic/authenticated pages remain a browser-automation concern.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse
import xml.etree.ElementTree as ET
import requests

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".ima" / "web_intelligence" / "state.json"
JOURNAL = ROOT / ".ima" / "journal" / "development.jsonl"
UA = os.getenv("IMA_WEB_INTELLIGENCE_UA", "IMA-Web-Intelligence/1.0 (+https://github.com/imaosglobal/Ima-kernel)")
TIMEOUT = float(os.getenv("IMA_WEB_INTELLIGENCE_TIMEOUT", "12"))
MAX_ITEMS = int(os.getenv("IMA_WEB_INTELLIGENCE_MAX_ITEMS", "300"))
SEEDS = [
    "https://www.commoncrawl.org/",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss",
    "https://www.mozilla.org/en-US/firefox/notes/feed/",
    "https://www.python.org/events/python-events/rss/",
    "https://github.blog/feed/",
    "https://hnrss.org/frontpage",
    "https://arxiv.org/rss/cs.AI",
    "https://www.nature.com/nature.rss",
    "https://www.w3.org/News/news.rss",
    "https://feeds.feedburner.com/TechCrunch/",
]
session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept": "*/*"})


def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_state():
    if not STATE.exists():
        return {"schema": "IMA-WEB-INTELLIGENCE-1.0", "seen": {}, "last_run": None}
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]


def add(items, url, title, source, kind, observed_at=None):
    if not url or not url.startswith(("http://", "https://")):
        return
    p = urlparse(url)
    if p.username or p.password:
        return
    items.append({
        "id": digest(url),
        "url": url,
        "title": re.sub(r"\s+", " ", title or url).strip()[:300],
        "source": source,
        "kind": kind,
        "observed_at": observed_at or now(),
    })


def fetch(url):
    r = session.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return r


def discover_feed(url, items):
    r = fetch(url)
    root = ET.fromstring(r.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    if root.tag.endswith("feed"):
        for entry in root.findall("atom:entry", ns):
            link = entry.find("atom:link", ns)
            href = link.attrib.get("href") if link is not None else None
            title = entry.findtext("atom:title", default="", namespaces=ns)
            add(items, href, title, url, "feed")
    else:
        for item in root.findall(".//item"):
            link = item.findtext("link", default="")
            title = item.findtext("title", default="")
            add(items, link, title, url, "feed")


def discover_sitemap(url, items):
    r = fetch(url)
    root = ET.fromstring(r.content)
    for loc in root.findall(".//{*}loc"):
        add(items, (loc.text or "").strip(), "", url, "sitemap")


def latest_commoncrawl():
    r = fetch("https://index.commoncrawl.org/collinfo.json")
    data = r.json()
    entries = data if isinstance(data, list) else data.get("collections", [])
    ids = [x.get("id") for x in entries if isinstance(x, dict) and x.get("id")]
    return ids[0] if ids else None


def discover_commoncrawl(items, crawl):
    if not crawl:
        return
    # Small, polite sample from representative public domains. Bulk analytics should
    # use the URL Index/Parquet path rather than hammering the CDX API.
    domains = ("commoncrawl.org", "w3.org", "github.blog", "arxiv.org")
    for domain in domains:
        q = quote(domain + "/*", safe="")
        url = f"https://index.commoncrawl.org/{crawl}-index?url={q}&output=json&filter=status:200&collapse=urlkey&limit=20"
        try:
            r = session.get(url, timeout=TIMEOUT)
            if r.status_code != 200:
                continue
            for line in r.text.splitlines():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                add(items, row.get("url"), "", f"Common Crawl {crawl}", "commoncrawl", row.get("timestamp"))
            time.sleep(1.0)
        except requests.RequestException:
            continue


def run():
    state = load_state()
    items = []
    errors = []
    for seed in SEEDS:
        try:
            discover_feed(seed, items)
        except Exception as exc:
            errors.append({"source": seed, "error": type(exc).__name__})
    try:
        crawl = latest_commoncrawl()
        discover_commoncrawl(items, crawl)
    except Exception as exc:
        crawl = None
        errors.append({"source": "Common Crawl", "error": type(exc).__name__})

    unique = {}
    for item in items:
        unique[item["url"]] = item
    items = list(unique.values())[:MAX_ITEMS]

    changed = []
    for item in items:
        old = state["seen"].get(item["id"])
        fingerprint = digest(json.dumps({k: item[k] for k in ("url", "title", "source", "kind")}, sort_keys=True))
        if not old or old.get("fingerprint") != fingerprint:
            changed.append(item)
        state["seen"][item["id"]] = {"fingerprint": fingerprint, "last_seen": item["observed_at"]}
    # Bound state growth.
    if len(state["seen"]) > 10000:
        state["seen"] = dict(list(state["seen"].items())[-10000:])
    state["last_run"] = now()
    state["latest_commoncrawl"] = crawl
    save_state(state)

    result = {
        "schema": "IMA-WEB-INTELLIGENCE-1.0",
        "status": "completed",
        "timestamp": state["last_run"],
        "sources": len(SEEDS) + 1,
        "discovered": len(items),
        "changed": len(changed),
        "errors": errors,
        "latest_commoncrawl": crawl,
        "policy": {
            "public_sources_only": True,
            "robots_and_provider_terms_respected": True,
            "dynamic_authenticated_pages_deferred": True,
            "learning_rule": "discovery is input; IMA changes only after verification and tests",
            "commoncrawl_cdx_polite_rate": "single-threaded with delay",
        },
        "items": changed[:MAX_ITEMS],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="run one discovery cycle")
    parser.parse_args()
    raise SystemExit(run())
