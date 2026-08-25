
from __future__ import annotations

from founder.executive_ai.economic_intelligence.economic_calibration import calibrate_economic_assumptions

from typing import Any, Dict

from .economic_model import evaluate_opportunity
from .economic_memory import save_economic_event


def evaluate_action_economics(action: Dict[str, Any]) -> Dict[str, Any]:
    target = str(action.get("target", "unknown"))
    score = float(action.get("score") or 0)
    action_name = action.get("action")

    # Initial economic assumptions.
    if action_name == "create_personal_outreach":
        conversion = min(0.50, max(0.01, score / 200.0))
        price = 99.0
        acquisition_cost = 5.0
        operating_cost = 2.0

    elif action_name == "prepare_public_impact_message":
        conversion = min(0.30, max(0.01, score / 300.0))
        price = 0.0
        acquisition_cost = 1.0
        operating_cost = 1.0

    elif action_name == "monitor":
        conversion = 0.0
        price = 0.0
        acquisition_cost = 0.0
        operating_cost = 0.5

    else:
        conversion = 0.0
        price = 0.0
        acquisition_cost = 0.0
        operating_cost = 0.0

    result = evaluate_opportunity(
        customer=target,
        offer="IMA",
        price=price,
        conversion=conversion,
        acquisition_cost=acquisition_cost,
        operating_cost=operating_cost,
    )

    result["action"] = action_name
    result["target"] = target
    result["opportunity_score"] = score

    # Learn from observed economic outcomes when available.
    base_economics = dict(result)

    try:
        calibrated = calibrate_economic_assumptions(base_economics)
    except Exception as exc:
        calibrated = {
            **base_economics,
            "calibrated": False,
            "calibration_samples": 0,
            "calibration_error": str(exc),
        }

    for key in (
        "expected_revenue",
        "contribution_profit",
        "roi",
        "margin",
    ):
        if key in calibrated:
            result[key] = calibrated[key]

    result["calibrated"] = calibrated.get("calibrated", False)
    result["calibration_samples"] = calibrated.get(
        "calibration_samples",
        0,
    )

    try:
        save_economic_event(result)
    except Exception as exc:
        result["economic_event_error"] = str(exc)

    return result


