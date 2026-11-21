"""Canonical collaboration, reciprocity and value-capture ledger.

IMA can discover partners and generate reciprocal collaboration opportunities.
External communication remains permissioned: discovery/analysis is automatic,
but sending binding offers, sharing private data, or accepting terms requires
explicit authorization and a configured provider.
"""

from dataclasses import dataclass, asdict
from enum import Enum


class CollaborationStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    QUALIFIED = "QUALIFIED"
    OUTREACH_READY = "OUTREACH_READY"
    CONTACTED = "CONTACTED"
    NEGOTIATING = "NEGOTIATING"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class CollaborationOpportunity:
    partner: str
    domain: str
    lesson: str
    reciprocal_value: str
    IMA_value: str
    status: CollaborationStatus = CollaborationStatus.DISCOVERED
    requires_human_approval: bool = True


def qualify(opportunity: CollaborationOpportunity) -> dict:
    return asdict(CollaborationOpportunity(
        partner=opportunity.partner,
        domain=opportunity.domain,
        lesson=opportunity.lesson,
        reciprocal_value=opportunity.reciprocal_value,
        IMA_value=opportunity.IMA_value,
        status=CollaborationStatus.OUTREACH_READY,
        requires_human_approval=True,
    ))


def value_types() -> tuple[str, ...]:
    return (
        "knowledge", "technology", "research", "distribution",
        "users", "accessibility", "creative_value", "social_impact",
        "revenue", "licensing", "services", "hardware_integration",
        "data_access_with_consent", "reputation", "network",
    )
