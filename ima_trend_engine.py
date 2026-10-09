"""Evidence-led trend-to-brand scoring primitives for IMA.

This module is deliberately deterministic and network-free. It scores supplied
evidence; it does not collect data, claim live monitoring, or execute commerce.
"""
from __future__ import annotations

from datetime import datetime
from urllib.parse import urlparse
from typing import Any

DIMENSIONS = (
    "trend_acceleration",
    "demand_persistence",
    "audience_relevance",
    "purchase_intent",
    "unmet_need",
    "differentiation",
    "unit_economics",
    "sourcing_feasibility",
    "safety_compliance",
    "fulfillment_feasibility",
    "cultural_fit",
    "sustainability",
    "reputation_safety",
    "testability",
    "time_to_learn",
)

PURCHASE_INTENT_KINDS = {
    "purchase_intent", "waitlist", "preorder", "sales",
    "survey_purchase_intent", "verified_conversion",
}


def validate_signal(signal: dict[str, Any]) -> list[str]:
    """Return actionable validation errors for one sourced signal."""
    errors: list[str] = []
    if not isinstance(signal, dict):
        return ["signal must be an object"]

    for field in ("source_url", "captured_at", "market", "language", "kind"):
        if not isinstance(signal.get(field), str) or not signal[field].strip():
            errors.append(f"{field} is required")

    url = signal.get("source_url", "")
    if url:
        parsed = urlparse(url)
        if parsed.scheme not in {"https", "http"} or not parsed.hostname:
            errors.append("source_url must be an absolute HTTP(S) URL")

    stamp = signal.get("captured_at", "")
    if stamp:
        try:
            parsed_stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            if parsed_stamp.tzinfo is None:
                errors.append("captured_at must include a timezone (UTC recommended)")
        except (TypeError, ValueError):
            errors.append("captured_at must be ISO-8601 with timezone")

    sample_size = signal.get("sample_size")
    if sample_size is not None and (
        isinstance(sample_size, bool) or not isinstance(sample_size, int) or sample_size < 0
    ):
        errors.append("sample_size must be a non-negative integer")

    if not isinstance(signal.get("summary", ""), str):
        errors.append("summary must be a string")
    return errors


def score_opportunity(dimensions: dict[str, Any]) -> dict[str, Any]:
    """Score supplied 0..5 dimensions; missing dimensions do not count as zero."""
    if not isinstance(dimensions, dict):
        raise TypeError("dimensions must be an object")

    valid: dict[str, float] = {}
    errors: list[str] = []
    for key, value in dimensions.items():
        if key not in DIMENSIONS:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 5:
            errors.append(f"{key} must be a number from 0 to 5")
        else:
            valid[key] = float(value)

    if errors:
        raise ValueError("; ".join(errors))

    coverage = len(valid) / len(DIMENSIONS)
    if len(valid) < 5:
        return {
            "score": None,
            "coverage": round(coverage, 3),
            "dimensions_scored": len(valid),
            "dimensions_total": len(DIMENSIONS),
            "recommendation": "collect_more_evidence",
            "reason": "At least 5 scored dimensions are required for a preliminary score.",
        }

    score = round(sum(valid.values()) / (5 * len(valid)) * 100, 1)
    recommendation = "test_small" if score >= 65 else "hold_or_research"
    return {
        "score": score,
        "coverage": round(coverage, 3),
        "dimensions_scored": len(valid),
        "dimensions_total": len(DIMENSIONS),
        "recommendation": recommendation,
        "reason": "Preliminary heuristic score, not proof of market demand or profitability.",
    }


def assess_demand(signals: list[dict[str, Any]]) -> dict[str, Any]:
    """Assess evidence sufficiency without overstating causal or commercial proof."""
    if not isinstance(signals, list):
        raise TypeError("signals must be a list")

    errors = []
    valid_signals = []
    for index, signal in enumerate(signals):
        signal_errors = validate_signal(signal)
        if signal_errors:
            errors.extend(f"signals[{index}]: {error}" for error in signal_errors)
        else:
            valid_signals.append(signal)

    domains = {
        urlparse(signal["source_url"]).hostname.lower()
        for signal in valid_signals
    }
    intent_signals = [
        signal for signal in valid_signals
        if signal.get("kind", "").lower() in PURCHASE_INTENT_KINDS
    ]

    sufficient = len(valid_signals) >= 3 and len(domains) >= 2 and bool(intent_signals)
    return {
        "status": "VALIDATED" if sufficient else "DISCOVERED",
        "valid_signal_count": len(valid_signals),
        "independent_domain_count": len(domains),
        "purchase_intent_signal_count": len(intent_signals),
        "errors": errors,
        "caveat": (
            "Evidence threshold met; this is not proof of sales, profitability, or causality."
            if sufficient else
            "Demand remains a hypothesis; require at least 3 valid signals, 2 domains, "
            "and 1 purchase-intent signal before marking VALIDATED."
        ),
    }


def build_opportunity_brief(
    *, title: str, customer_problem: str, market: str,
    dimensions: dict[str, Any], signals: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create a reproducible opportunity brief with explicit evidence boundaries."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title is required")
    if not isinstance(customer_problem, str) or not customer_problem.strip():
        raise ValueError("customer_problem is required")
    if not isinstance(market, str) or not market.strip():
        raise ValueError("market is required")

    demand = assess_demand(signals)
    score = score_opportunity(dimensions)
    return {
        "schema_version": "1.0",
        "title": title.strip(),
        "customer_problem": customer_problem.strip(),
        "market": market.strip(),
        "demand_assessment": demand,
        "opportunity_score": score,
        "evidence_state": demand["status"],
        "commercial_state": "NOT_ESTABLISHED",
        "next_action": (
            "design a small, authorized validation test"
            if demand["status"] == "VALIDATED" and score["recommendation"] == "test_small"
            else "collect independent evidence and refine assumptions"
        ),
        "signals": signals,
    }
