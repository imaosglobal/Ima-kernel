from datetime import datetime
from learning.reasoning_engine import reason, evaluate_reasoning
from learning.planning_engine import build_plan


def run_autonomy(context=None):
    """
    Controlled autonomy loop:
    observe -> reason -> evaluate -> plan.
    Execution remains explicit and separately gated.
    """
    context = context or {}

    reasoning = reason(context)
    evaluation = evaluate_reasoning(reasoning)
    plan = build_plan(reasoning)

    return {
        "timestamp": str(datetime.now()),
        "reasoning": reasoning,
        "evaluation": evaluation,
        "plan": plan,
        "status": "autonomy_cycle_completed"
    }
