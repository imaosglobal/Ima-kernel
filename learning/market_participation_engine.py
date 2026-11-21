"""IMA market participation engine.

Moves IMA from benchmarking the market to preparing measurable participation:
product offers, integrations, partnerships, pilots, distribution and value capture.
It does not claim market success until evidence exists and does not perform binding
external actions without authorization.
"""
from dataclasses import dataclass, asdict
from enum import Enum


class MarketParticipationStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    VALIDATED = "VALIDATED"
    OFFER_READY = "OFFER_READY"
    PILOT_READY = "PILOT_READY"
    PARTNERSHIP_READY = "PARTNERSHIP_READY"
    LIVE = "LIVE"
    MEASURED = "MEASURED"


@dataclass(frozen=True)
class MarketOpportunity:
    segment: str
    user_problem: str
    IMA_capability: str
    offer: str
    distribution_path: str
    reciprocal_value: str
    success_metric: str
    status: MarketParticipationStatus = MarketParticipationStatus.CANDIDATE
    external_commitment_requires_approval: bool = True


def validate_opportunity(opportunity: MarketOpportunity) -> dict:
    fields = (
        opportunity.segment, opportunity.user_problem, opportunity.IMA_capability,
        opportunity.offer, opportunity.distribution_path,
        opportunity.reciprocal_value, opportunity.success_metric
    )
    if not all(x.strip() for x in fields):
        raise ValueError("market opportunity fields must be non-empty")
    return asdict(opportunity)


def participation_paths() -> tuple[str, ...]:
    return (
        "direct_product",
        "developer_sdk",
        "device_integration",
        "enterprise_service",
        "consumer_service",
        "research_pilot",
        "accessibility_program",
        "creator_ecosystem",
        "open_source_ecosystem",
        "licensing",
        "strategic_partnership",
    )
