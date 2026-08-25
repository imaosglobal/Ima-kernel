from founder.executive_ai.economic_intelligence.economic_outcome import get_outcomes


def learn_economic_patterns():
    outcomes = get_outcomes()

    if not outcomes:
        return {
            "samples": 0,
            "avg_revenue": 0.0,
            "avg_profit": 0.0,
            "avg_roi": 0.0,
            "avg_margin": 0.0,
            "success_rate": 0.0,
        }

    revenues = [float(x.get("revenue", 0)) for x in outcomes]
    profits = [float(x.get("profit", 0)) for x in outcomes]
    rois = [float(x.get("roi", 0)) for x in outcomes]
    margins = [float(x.get("margin", 0)) for x in outcomes]

    successful = sum(
        1
        for x in outcomes
        if x.get("status") in {
            "success",
            "positive_response",
            "converted",
            "paid",
        }
        or float(x.get("profit", 0)) > 0
    )

    n = len(outcomes)

    return {
        "samples": n,
        "avg_revenue": sum(revenues) / n,
        "avg_profit": sum(profits) / n,
        "avg_roi": sum(rois) / n,
        "avg_margin": sum(margins) / n,
        "success_rate": successful / n,
    }
