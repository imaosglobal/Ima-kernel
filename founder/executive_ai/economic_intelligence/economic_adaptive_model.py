from founder.executive_ai.economic_intelligence.economic_learning import (
    learn_economic_patterns,
)


def adaptive_assumptions(action):
    """
    Produce economic assumptions from observed historical outcomes.

    Historical observations modify assumptions gradually.
    No observation means the caller keeps its baseline assumptions.
    """

    state = learn_economic_patterns()

    samples = int(state.get("samples", 0) or 0)

    if samples <= 0:
        return {
            "samples": 0,
            "conversion_multiplier": 1.0,
            "revenue_multiplier": 1.0,
            "profit_multiplier": 1.0,
            "roi_multiplier": 1.0,
            "confidence": 0.0,
        }

    success_rate = float(state.get("success_rate", 0.0) or 0.0)

    avg_revenue = float(state.get("avg_revenue", 0.0) or 0.0)
    avg_profit = float(state.get("avg_profit", 0.0) or 0.0)
    avg_roi = float(state.get("avg_roi", 0.0) or 0.0)

    # Conservative learning:
    # historical data influences the model progressively rather
    # than replacing the baseline assumptions immediately.
    conversion_multiplier = 1.0 + ((success_rate - 0.5) * 0.20)

    revenue_multiplier = (
        1.0
        if avg_revenue <= 0
        else 1.0 + min(0.25, max(-0.25, (avg_revenue - 40.0) / 160.0))
    )

    profit_multiplier = (
        1.0
        if avg_profit <= 0
        else 1.0 + min(0.25, max(-0.25, (avg_profit - 33.0) / 132.0))
    )

    roi_multiplier = (
        1.0
        if avg_roi <= 0
        else 1.0 + min(0.25, max(-0.25, (avg_roi - 4.0) / 16.0))
    )

    confidence = min(1.0, samples / 10.0)

    return {
        "samples": samples,
        "conversion_multiplier": conversion_multiplier,
        "revenue_multiplier": revenue_multiplier,
        "profit_multiplier": profit_multiplier,
        "roi_multiplier": roi_multiplier,
        "confidence": confidence,
    }
