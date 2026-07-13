from learning.learning_memory import store_pattern
from learning.safety_gate import check_action


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

        return {
            "action": action,
            "status": "executed"
        }


    if decision == "system_improvement":

        action = f"תוכנית שיפור מערכת: {reason}"

        store_pattern(action)

        return {
            "action": action,
            "status": "executed"
        }


    return {
        "action": decision,
        "status": "planned",
        "reason": reason
    }
