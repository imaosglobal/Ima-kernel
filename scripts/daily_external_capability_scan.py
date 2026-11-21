"""Permanent industry-wide external capability discovery."""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from learning.external_capability_discovery import normalize_candidates
from learning.industry_capability_patterns import (
    INDUSTRY_DOMAINS,
    normalize_candidates as normalize_industry_candidates,
)

INDUSTRY_GROUPS = {
    "creative_3d": ["3d_games", "game_engines", "virtual_worlds", "simulation", "graphics", "design", "web_design", "architecture", "home_design"],
    "finance_commerce": ["finance", "banking", "payments", "insurance", "accounting", "investing", "ecommerce", "marketplaces", "retail"],
    "revenue": ["marketing", "sales", "crm", "advertising", "customer_support", "creator_economy"],
    "home_field": ["construction", "real_estate", "plumbing", "electrical", "hvac", "field_service", "diy_repair", "automotive"],
    "industrial": ["manufacturing", "robotics", "hardware", "consumer_electronics", "iot", "telecommunications", "cloud_infrastructure", "developer_tools", "data_platforms"],
    "human": ["accessibility", "healthcare", "mental_wellbeing", "education", "legal", "family", "social_community", "language_translation", "religion_culture"],
    "public_safety": ["government", "civic_services", "security", "cybersecurity", "disaster_response", "humanitarian", "nonprofit"],
    "science_frontier": ["science", "biotech", "chemistry", "research_tools", "space", "aerospace", "marine", "climate", "energy", "agriculture"],
    "life_and_service": ["food", "hospitality", "travel", "maps_navigation", "sports", "fitness", "fashion"],
    "media": ["music", "film_video", "publishing", "news_media"],
    "business_operations": ["logistics", "supply_chain", "professional_services", "hr_recruiting", "productivity", "project_management"],
}

def search_github(query: str, limit: int = 5) -> list[dict]:
    params = urllib.parse.urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": limit})
    req = urllib.request.Request(
        "https://api.github.com/search/repositories?" + params,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "IMA-Daily-Industry-Capability-Scanner"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response).get("items", [])

def search_gdelt(query: str, limit: int = 10) -> list[dict]:
    params = urllib.parse.urlencode({
        "query": query,
        "mode": "artlist",
        "format": "json",
        "maxrecords": limit,
        "sort": "datedesc",
    })
    req = urllib.request.Request(
        "https://api.gdeltproject.org/api/v2/doc/doc?" + params,
        headers={"User-Agent": "IMA-Daily-Industry-Capability-Scanner"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response).get("articles", [])

def build_group_query(domains: list[str]) -> str:
    terms = [d.replace("_", " ") for d in domains]
    return "(" + " OR ".join(f'"{t}"' for t in terms) + ") AI OR automation OR workflow OR software"

def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    candidates = []
    errors = []
    group_results = {}
    web_group_results = {}

    for group, domains in INDUSTRY_GROUPS.items():
        try:
            items = search_github(build_group_query(domains))
            group_results[group] = len(items)
            for item in items:
                candidates.append({
                    "source": "github",
                    "name": item.get("full_name", ""),
                    "evidence_url": item.get("html_url", ""),
                    "capability": group,
                    "description": item.get("description", "") or "",
                    "topics": item.get("topics", []) or [],
                })
        except Exception as exc:
            errors.append({"source": "github", "group": group, "error": str(exc)})
            group_results[group] = 0

        try:
            web_items = search_gdelt(build_group_query(domains), limit=10)
            web_group_results[group] = len(web_items)
            for item in web_items:
                candidates.append({
                    "source": "gdelt_web",
                    "name": item.get("title", ""),
                    "evidence_url": item.get("url", ""),
                    "capability": group,
                    "description": item.get("seendate", "") or "",
                    "topics": [],
                })
        except Exception as exc:
            errors.append({"source": "gdelt_web", "group": group, "error": str(exc)})
            web_group_results[group] = 0

    industry_review = []
    for item in candidates:
        for domain in INDUSTRY_GROUPS.get(item.get("capability", ""), []):
            industry_review.append({
                "domain": domain,
                "source": item.get("source", ""),
                "lesson": item.get("description", "") or item.get("name", ""),
                "canonical_target": "canonical IMA learning/orchestration layer",
                "conflict_check": "deduplicate against canonical brain, memory, feedback, LIVE-001, security and approval contracts",
            })

    taxonomy_path = Path("artifacts/web-intelligence/industry-capability-taxonomy-2026-11-21.json")
    taxonomy_path.parent.mkdir(parents=True, exist_ok=True)
    taxonomy_path.write_text(json.dumps({
        "generated_at": generated_at,
        "domain_count": len(INDUSTRY_DOMAINS),
        "domains": INDUSTRY_DOMAINS,
        "groups": INDUSTRY_GROUPS,
        "new_domain_policy": "If a discovered sector is absent, append it as REVIEW_REQUIRED before promotion.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    payload = {
        "generated_at": generated_at,
        "source_scope": ["github", "gdelt_web"],
        "industry_group_count": len(INDUSTRY_GROUPS),
        "industry_domain_count": len(INDUSTRY_DOMAINS),
        "group_results": group_results,
        "web_group_results": web_group_results,
        "candidate_count": len(candidates),
        "candidates": normalize_candidates(candidates),
        "industry_review_candidates": normalize_industry_candidates(industry_review),
        "errors": errors,
        "promotion_rule": "Candidates require canonical conflict/evidence/security review before integration.",
        "implementation_rule": "Safe generic patterns should be implemented immediately as canonical contracts; provider-specific integrations remain verification-gated.",
    }
    path = Path("artifacts/web-intelligence/daily-external-capability-scan.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
