"""Detect previously unlisted industry terms from daily discovery topics.

New terms are review candidates, not automatic capability promotions.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from learning.industry_capability_patterns import INDUSTRY_DOMAINS

GENERIC = {
    "ai", "agent", "agents", "automation", "software", "tools", "open-source",
    "python", "javascript", "typescript", "api", "web", "mobile", "cloud",
    "machine-learning", "deep-learning", "llm", "chatbot", "framework",
}

def main() -> None:
    source = Path("artifacts/web-intelligence/daily-external-capability-scan.json")
    data = json.loads(source.read_text(encoding="utf-8")) if source.exists() else {}
    known = set(INDUSTRY_DOMAINS)
    observed = set()
    for item in data.get("candidates", []):
        for topic in item.get("topics", []) or []:
            term = re.sub(r"[^a-z0-9]+", "_", str(topic).lower()).strip("_")
            if term and term not in known and term not in GENERIC and len(term) >= 4:
                observed.add(term)
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "known_domain_count": len(INDUSTRY_DOMAINS),
        "observed_new_domain_candidates": sorted(observed),
        "status": "REVIEW_REQUIRED",
        "promotion_rule": "New domains must be validated as genuine sectors before being appended to the canonical taxonomy.",
    }
    Path("artifacts/web-intelligence").mkdir(parents=True, exist_ok=True)
    Path("artifacts/web-intelligence/daily-new-domain-candidates.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

if __name__ == "__main__":
    main()
