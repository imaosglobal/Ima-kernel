from datetime import datetime


def plan_learning_action(decision, reason):
    """
    Planning-only action layer.

    This function creates an explicit plan.
    It does not execute system changes.
    """

    return {
        "decision": decision,
        "reason": reason,
        "status": "planned",
        "execution": "disabled",
        "timestamp": str(datetime.now()),
    }


def execute_learning_action(decision, reason):
    """
    Compatibility wrapper.

    Execution is intentionally disabled.
    Existing callers receive a plan instead of performing side effects.
    """

    return plan_learning_action(decision, reason)
