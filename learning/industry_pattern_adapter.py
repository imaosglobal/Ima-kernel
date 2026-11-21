"""Canonical adapter for transferable cross-industry patterns.

This is the immediate implementation layer: it converts a discovered industry
lesson into a canonical IMA workflow capability candidate. It does not execute
external actions or create a parallel runtime.
"""

from dataclasses import dataclass, asdict
from typing import Iterable

from learning.industry_capability_patterns import TRANSFERABLE_PATTERNS


@dataclass(frozen=True)
class AdaptedPattern:
    domain: str
    pattern: str
    canonical_contract: str
    requires_approval: bool
    status: str = "CANONICAL_ADAPTER_READY"


DOMAIN_TO_PATTERNS = {
    "3d_games": ["visual_spatial_reasoning", "simulation", "creative_iteration"],
    "game_engines": ["visual_spatial_reasoning", "simulation"],
    "virtual_worlds": ["visual_spatial_reasoning", "cross_device_continuity"],
    "finance": ["transaction_lifecycle", "diagnosis", "observability", "human_approval"],
    "banking": ["transaction_lifecycle", "privacy_boundary", "human_approval"],
    "payments": ["transaction_lifecycle", "privacy_boundary", "human_approval"],
    "marketing": ["workflow_orchestration", "personalization", "observability"],
    "sales": ["workflow_orchestration", "customer_relationship", "human_approval"],
    "plumbing": ["diagnosis", "field_service", "workflow_orchestration"],
    "home_design": ["visual_spatial_reasoning", "creative_iteration"],
    "web_design": ["creative_iteration", "accessibility", "observability"],
    "accessibility": ["accessibility", "privacy_boundary"],
    "healthcare": ["diagnosis", "privacy_boundary", "human_approval"],
    "education": ["personalization", "accessibility", "observability"],
    "robotics": ["simulation", "human_approval", "safety_red_team"],
    "hardware": ["diagnosis", "observability", "cross_device_continuity"],
    "security": ["safety_red_team", "observability", "human_approval"],
    "cybersecurity": ["safety_red_team", "observability", "human_approval"],
    "science": ["diagnosis", "simulation", "observability"],
    "space": ["simulation", "observability", "human_approval"],
    "logistics": ["workflow_orchestration", "field_service", "observability"],
    "construction": ["visual_spatial_reasoning", "simulation", "field_service"],
    "real_estate": ["visual_spatial_reasoning", "transaction_lifecycle"],
    "music": ["creative_iteration", "personalization", "provenance"],
    "film_video": ["creative_iteration", "provenance"],
    "customer_support": ["customer_relationship", "diagnosis", "accessibility"],
    "ecommerce": ["transaction_lifecycle", "personalization", "customer_relationship"],
    "family": ["customer_relationship", "privacy_boundary", "cross_device_continuity"],
}


def adapt_domain(domain: str) -> list[dict]:
    names = DOMAIN_TO_PATTERNS.get(domain, [
        "workflow_orchestration",
        "observability",
        "privacy_boundary",
        "human_approval",
    ])
    out = []
    for name in names:
        if name not in TRANSFERABLE_PATTERNS:
            continue
        out.append(asdict(AdaptedPattern(
            domain=domain,
            pattern=name,
            canonical_contract=TRANSFERABLE_PATTERNS[name],
            requires_approval=name in {"transaction_lifecycle", "human_approval", "field_service", "simulation"},
        )))
    return out


def adapt_domains(domains: Iterable[str]) -> list[dict]:
    result = []
    for domain in domains:
        result.extend(adapt_domain(str(domain).strip()))
    return result
