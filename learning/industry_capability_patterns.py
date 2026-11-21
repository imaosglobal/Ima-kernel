"""Cross-industry capability taxonomy and safe adaptation rules.

The taxonomy is intentionally industry-agnostic: IMA learns transferable patterns
from any sector without creating a second runtime authority or copying proprietary
implementation. New sectors discovered by the daily scan are added as candidates
and become reviewable before promotion.
"""

from dataclasses import dataclass, asdict
from typing import Iterable


INDUSTRY_DOMAINS = [
    "3d_games", "game_engines", "virtual_worlds", "simulation", "graphics",
    "finance", "banking", "payments", "insurance", "accounting", "investing",
    "marketing", "sales", "crm", "customer_support", "ecommerce", "marketplaces",
    "advertising", "logistics", "supply_chain", "construction", "real_estate",
    "home_design", "plumbing", "electrical", "hvac", "field_service", "automotive",
    "manufacturing", "robotics", "hardware", "consumer_electronics", "iot",
    "accessibility", "healthcare", "mental_wellbeing", "education", "legal",
    "government", "civic_services", "security", "cybersecurity", "science",
    "biotech", "chemistry", "energy", "climate", "agriculture", "food",
    "hospitality", "travel", "maps_navigation", "music", "film_video",
    "creator_economy", "fashion", "sports", "fitness", "social_community",
    "family", "religion_culture", "language_translation", "publishing",
    "news_media", "telecommunications", "space", "aerospace", "marine",
    "retail", "professional_services", "hr_recruiting", "productivity",
    "project_management", "design", "web_design", "architecture", "diy_repair",
    "disaster_response", "humanitarian", "nonprofit", "research_tools",
    "developer_tools", "data_platforms", "cloud_infrastructure",
]

TRANSFERABLE_PATTERNS = {
    "workflow_orchestration": "map a user goal into observable stages, permissions, actions and verification",
    "diagnosis": "turn symptoms/evidence into bounded hypotheses and next checks",
    "personalization": "adapt presentation and workflow without silently changing user intent",
    "visual_spatial_reasoning": "use spatial/3D representations when they improve understanding",
    "transaction_lifecycle": "model quote/order/payment/fulfillment/refund with explicit authorization",
    "field_service": "capture issue -> schedule -> route -> perform -> document -> follow up",
    "creative_iteration": "draft -> inspect -> revise -> preserve provenance",
    "customer_relationship": "remember consented context, preferences and interaction history with correction/withdrawal",
    "simulation": "test hypothetical states before consequential real-world action",
    "observability": "record evidence, failures, regressions and recovery state",
    "accessibility": "make capability reachable through multiple interaction modes",
    "privacy_boundary": "minimize data and keep private context scoped to the user",
    "human_approval": "require explicit confirmation before consequential actions",
    "safety_red_team": "test misuse, prompt injection, authorization and data leakage",
    "cross_device_continuity": "preserve user-controlled state across device classes without creating a second memory authority",
}


@dataclass(frozen=True)
class IndustryCandidate:
    domain: str
    source: str
    lesson: str
    canonical_target: str
    conflict_check: str
    status: str = "REVIEW_REQUIRED"


def normalize_candidates(items: Iterable[dict]) -> list[dict]:
    out = []
    for item in items:
        required = ("domain", "source", "lesson", "canonical_target", "conflict_check")
        if not all(str(item.get(k, "")).strip() for k in required):
            continue
        domain = str(item["domain"]).strip()
        if domain not in INDUSTRY_DOMAINS:
            continue
        out.append(asdict(IndustryCandidate(
            domain=domain,
            source=str(item["source"]).strip(),
            lesson=str(item["lesson"]).strip(),
            canonical_target=str(item["canonical_target"]).strip(),
            conflict_check=str(item["conflict_check"]).strip(),
        )))
    return out
