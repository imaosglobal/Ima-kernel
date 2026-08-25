
from __future__ import annotations

from typing import Any, Dict, List

from .economic_memory import get_economic_memory


def summarize_economics() -> Dict[str, Any]:
    records = get_economic_memory()

    if not records:
        return {
            "events": 0,
            "expected_revenue": 0.0,
            "expected_profit": 0.0,
            "average_margin": 0.0,
            "average_roi": 0.0,
        }

    revenues = [
        float(r.get("expected_revenue", 0))
        for r in records
    ]

    profits = [
        float(r.get("contribution_profit", 0))
        for r in records
    ]

    margins = [
        float(r.get("margin", 0))
        for r in records
    ]

    rois = [
        float(r.get("roi", 0))
        for r in records
    ]

    return {
        "events": len(records),
        "expected_revenue": sum(revenues),
        "expected_profit": sum(profits),
        "average_margin": sum(margins) / len(margins),
        "average_roi": sum(rois) / len(rois),
    }


def rank_economic_opportunities(
    opportunities: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    ranked = []

    for opportunity in opportunities:
        economics = opportunity.get("economics", {})

        economic_score = (
            float(economics.get("expected_revenue", 0))
            + float(economics.get("contribution_profit", 0))
            + float(economics.get("roi", 0)) * 10
        )

        item = dict(opportunity)
        item["economic_score"] = economic_score
        ranked.append(item)

    ranked.sort(
        key=lambda x: x["economic_score"],
        reverse=True,
    )

    return ranked
