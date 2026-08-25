from founder.executive_ai.economic_intelligence.economic_cycle import execute_economic_cycle
from founder.executive_ai.action_engine.action_feedback_learning import learn_from_action


def process_economic_outcome(action, actual):
    """
    Connect economic outcomes to the existing action-learning system.
    """

    cycle = execute_economic_cycle(
        action,
        actual=actual,
    )

    prediction = cycle.get("prediction", {})
    outcome = cycle.get("outcome", {})
    comparison = cycle.get("comparison", {})

    feedback = {
        "action": action,
        "prediction": prediction,
        "outcome": outcome,
        "comparison": comparison,
        "economic_error": {
            "revenue": comparison.get("revenue_error", 0.0),
            "profit": comparison.get("profit_error", 0.0),
            "roi": comparison.get("roi_error", 0.0),
        },
    }

    try:
        learning_result = learn_from_action(
            action,
            {
                "status": actual.get("status", "observed"),
                "economic_feedback": feedback,
            },
        )
    except Exception as exc:
        learning_result = {
            "status": "learning_error",
            "error": str(exc),
        }

    cycle["action_learning"] = learning_result

    return cycle
