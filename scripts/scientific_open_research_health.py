#!/usr/bin/env python3
"""Daily health gate for IMA's free/open scientific discovery layer.

This checks availability and basic provenance of public scientific indexes.
It never treats an API response as scientific truth; it only verifies that
the discovery channels are reachable and structurally usable.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

SOURCES = {
    "OpenAlex": "https://api.openalex.org/works?search=artificial%20intelligence&per-page=1",
    "Semantic Scholar": "https://api.semanticscholar.org/graph/v1/paper/search?query=artificial%20intelligence&limit=1&fields=title",
    "Crossref": "https://api.crossref.org/works?query=artificial%20intelligence&rows=1",
    "PubMed": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial%20intelligence&retmax=1",
    "arXiv": "https://export.arxiv.org/api/query?search_query=all:artificial%20intelligence&max_results=1",
}

def check(name, url):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "IMA-Scientific-Research-Health/1.0"},
        )
        response.raise_for_status()
        body = response.text
        usable = bool(body.strip())
        if name == "OpenAlex":
            usable = isinstance(response.json().get("results"), list)
        elif name == "Semantic Scholar":
            usable = isinstance(response.json().get("data"), list)
        elif name == "Crossref":
            usable = isinstance(response.json().get("message", {}).get("items"), list)
        elif name == "PubMed":
            usable = bool(re.search(r"<Id>\d+</Id>", body))
        elif name == "arXiv":
            usable = "<entry>" in body
        return {"source": name, "status": "PASS" if usable else "FAIL", "http_status": response.status_code}
    except Exception as exc:
        return {"source": name, "status": "ERROR", "error": type(exc).__name__}

def main():
    results = [check(name, url) for name, url in SOURCES.items()]
    failed = [r for r in results if r["status"] != "PASS"]
    record = {
        "schema": "IMA-SCIENTIFIC-OPEN-RESEARCH-HEALTH-1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "paid_provider_required": False,
        "sources": results,
        "status": "PASS" if not failed else "DEGRADED",
        "truth_boundary": "Source availability is not evidence that a scientific claim is true; claims require source-level verification.",
    }
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
