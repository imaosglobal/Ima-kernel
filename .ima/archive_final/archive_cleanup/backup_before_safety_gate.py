from learning.learning_memory import store_pattern


def execute_learning_action(decision, reason):

    if decision == "knowledge_expansion":
        action = f"נוצרה משימת הרחבת ידע: {reason}"

        store_pattern(action)

        return {
            "action": action,
            "status": "executed"
        }

    return {
        "action": "none",
        "status": "ignored"
    }
