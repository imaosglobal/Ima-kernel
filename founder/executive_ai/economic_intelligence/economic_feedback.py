def compare_economics(expected, actual):
    expected_revenue = float(
        expected.get("expected_revenue", 0)
    )

    expected_profit = float(
        expected.get("contribution_profit", 0)
    )

    expected_roi = float(
        expected.get("roi", 0)
    )

    actual_revenue = float(
        actual.get("revenue", 0)
    )

    actual_profit = float(
        actual.get("profit", 0)
    )

    actual_roi = float(
        actual.get("roi", 0)
    )

    return {
        "revenue_error":
            actual_revenue - expected_revenue,

        "profit_error":
            actual_profit - expected_profit,

        "roi_error":
            actual_roi - expected_roi,

        "revenue_accuracy":
            (
                actual_revenue / expected_revenue
                if expected_revenue
                else 0.0
            ),

        "profit_accuracy":
            (
                actual_profit / expected_profit
                if expected_profit
                else 0.0
            ),

        "roi_accuracy":
            (
                actual_roi / expected_roi
                if expected_roi
                else 0.0
            ),
    }
