from founder.executive_ai.action_engine.action_registry import ACTIONS


def create_action_plan(intent, stage="prototype"):

    if intent == "customers":

        return [
            "find_leads",
            "rank_leads",
            "generate_outreach",
            "send_outreach",
            "collect_feedback",
        ]

    if intent == "product_improvement":

        return [
            "collect_feedback",
            "analyze_feedback",
            "update_product",
        ]

    return [
        "collect_feedback",
    ]


def validate_action_plan(plan):
    """
    Verify that every planned action has a registered executor.
    """

    unknown = [
        action
        for action in plan
        if action not in ACTIONS
    ]

    return {
        "valid": not unknown,
        "unknown_actions": unknown,
        "plan": plan,
    }
