"""Lightweight daily GitHub discovery scan.

Discovery only: writes candidates for IMA review. It does not modify source code.
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from learning.external_capability_discovery import normalize_candidates

QUERIES = [
    "AI agent browser accessibility memory",
    "AI agent human approval security",
    "MCP Apps interactive UI agent",
    "AI personal assistant privacy memory",
]

def search_github(query: str) -> list[dict]:
    params = urllib.parse.urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": 5})
    req = urllib.request.Request(
        "https://api.github.com/search/repositories?" + params,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "IMA-Daily-Capability-Scanner"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.load(response)
    return [
        {
            "source": "github",
            "name": item.get("full_name", ""),
            "evidence_url": item.get("html_url", ""),
            "capability": query,
        }
        for item in data.get("items", [])
    ]

def main() -> None:
    candidates = []
    errors = []
    for query in QUERIES:
        try:
            candidates.extend(search_github(query))
        except Exception as exc:
            errors.append({"query": query, "error": str(exc)})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_scope": ["github"],
        "candidate_count": len(candidates),
        "candidates": normalize_candidates(candidates),
        "errors": errors,
        "promotion_rule": "Candidates require canonical conflict/evidence/security review before integration.",
    }
    path = Path("artifacts/web-intelligence/daily-external-capability-scan.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
