from founder.executive_ai.economic_intelligence.economic_engine import evaluate_action_economics
from founder.executive_ai.economic_intelligence.economic_outcome import record_outcome
from founder.executive_ai.economic_intelligence.economic_feedback import compare_economics
from founder.executive_ai.economic_intelligence.economic_learning import learn_economic_patterns


def execute_economic_cycle(action, actual=None):
    """
    Full economic feedback cycle:

    action
        -> prediction
        -> observed outcome
        -> prediction error
        -> learning state
    """

    prediction = evaluate_action_economics(action)

    actual = actual or {}

    outcome = record_outcome(
        action=action,
        revenue=actual.get("revenue", 0.0),
        acquisition_cost=actual.get(
            "acquisition_cost",
            prediction.get("acquisition_cost", 0.0),
        ),
        operating_cost=actual.get(
            "operating_cost",
            prediction.get("operating_cost", 0.0),
        ),
        conversion=actual.get("conversion"),
        status=actual.get("status", "observed"),
    )

    comparison = compare_economics(
        prediction,
        outcome,
    )

    learning = learn_economic_patterns()

    return {
        "action": action,
        "prediction": prediction,
        "outcome": outcome,
        "comparison": comparison,
        "learning": learning,
    }
