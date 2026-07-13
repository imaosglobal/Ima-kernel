from learning.learning_memory import store_pattern
from learning.safety_gate import check_action
from learning.evaluation_engine import evaluate_action


def execute_learning_action(decision, reason):

    safety = check_action(decision, reason)

    if not safety["approved"]:
        return {
            "action": decision,
            "status": "blocked",
            "reason": safety["reason"]
        }

    if decision == "knowledge_expansion":

        action = f"נוצרה משימת הרחבת ידע: {reason}"

        store_pattern(action)

        evaluation = evaluate_action(
            decision,
            action,
            1.0
        )

        return {
            "action": action,
            "status": "executed",
            "evaluation": evaluation
        }


    if decision == "system_improvement":

        action = f"תוכנית שיפור מערכת: {reason}"

        store_pattern(action)

        evaluation = evaluate_action(
            decision,
            action,
            1.0
        )

        return {
            "action": action,
            "status": "executed",
            "evaluation": evaluation
        }


    return {
        "action": decision,
        "status": "planned",
        "reason": reason
    }
