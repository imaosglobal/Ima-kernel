from founder.executive_ai.economic_intelligence.economic_learning import (
    learn_economic_patterns,
)


def calibrate_economic_assumptions(base):
    """
    Adjust economic assumptions using observed outcomes.

    Base assumptions remain intact when there is insufficient data.
    """

    base = dict(base or {})
    learning = learn_economic_patterns()

    samples = learning.get("samples", 0)

    if samples < 3:
        return {
            **base,
            "calibrated": False,
            "calibration_samples": samples,
        }

    observed_revenue = learning["avg_revenue"]
    observed_profit = learning["avg_profit"]
    observed_roi = learning["avg_roi"]

    expected_revenue = float(base.get("expected_revenue", 0))
    expected_profit = float(base.get("contribution_profit", 0))
    expected_roi = float(base.get("roi", 0))

    # Conservative calibration:
    # blend prior assumptions with observed reality.
    alpha = min(0.75, samples / 20.0)

    if expected_revenue > 0:
        calibrated_revenue = (
            expected_revenue * (1 - alpha)
            + observed_revenue * alpha
        )
    else:
        calibrated_revenue = observed_revenue

    if expected_profit != 0:
        calibrated_profit = (
            expected_profit * (1 - alpha)
            + observed_profit * alpha
        )
    else:
        calibrated_profit = observed_profit

    if expected_roi != 0:
        calibrated_roi = (
            expected_roi * (1 - alpha)
            + observed_roi * alpha
        )
    else:
        calibrated_roi = observed_roi

    return {
        **base,
        "expected_revenue": calibrated_revenue,
        "contribution_profit": calibrated_profit,
        "roi": calibrated_roi,
        "calibrated": True,
        "calibration_samples": samples,
        "calibration_weight": alpha,
    }
