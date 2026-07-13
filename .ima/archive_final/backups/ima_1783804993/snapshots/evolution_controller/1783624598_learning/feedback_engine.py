from learning.evaluation_engine import get_evaluations
from learning.self_reflection import suggest_improvement


def process_feedback():

    evaluations = get_evaluations()

    results = []

    for item in evaluations:

        score = item.get("score", 0)

        if score < 0.7:
            suggest_improvement(
                "feedback",
                f"פעולה {item.get('action')} קיבלה ציון נמוך: {score}"
            )

            results.append("needs_improvement")

        else:
            results.append("successful_pattern")

    return results
