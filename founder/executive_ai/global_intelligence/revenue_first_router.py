"""Revenue-first execution policy for IMA.

Keeps paid model/API spend at zero until attributable revenue exists or the
user explicitly authorizes a budget. It can still plan, research, publish
eligible affiliate content, and prepare paid-provider work without making a
paid API call.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RevenueSource:
    name: str
    priority: int
    kind: str


REVENUE_SOURCES = (
    RevenueSource("Affiracle/AliExpress", 1, "affiliate"),
    RevenueSource("eBay", 2, "partner_or_affiliate"),
    RevenueSource("Amazon", 3, "partner_or_affiliate"),
    RevenueSource("impact.com", 4, "partnerships"),
)


def paid_ai_budget_gate(
    *,
    verified_revenue_usd: float = 0.0,
    explicit_budget_usd: float = 0.0,
    requested_spend_usd: float = 0.0,
) -> dict:
    """Return a deterministic decision; never creates a payment."""
    revenue = max(float(verified_revenue_usd), 0.0)
    budget = max(float(explicit_budget_usd), 0.0)
    requested = max(float(requested_spend_usd), 0.0)

    if requested <= 0:
        return {"allowed": False, "reason": "no_paid_call_requested", "available_usd": 0.0}

    available = max(revenue * 0.25, budget)
    if available <= 0:
        return {
            "allowed": False,
            "reason": "earn_before_spend",
            "available_usd": 0.0,
            "required_human_approval": True,
        }

    allowed = requested <= available
    return {
        "allowed": allowed,
        "reason": "funded_by_verified_revenue_or_explicit_budget" if allowed else "requested_spend_exceeds_cap",
        "available_usd": round(available, 6),
        "required_human_approval": True,
    }


def revenue_first_plan() -> dict:
    return {
        "paid_ai": "blocked_until_funded",
        "research": "allowed",
        "affiliate_content": "allowed_with_disclosure",
        "purchase": "human_approval_required",
        "sources": [source.__dict__.copy() for source in REVENUE_SOURCES],
    }
