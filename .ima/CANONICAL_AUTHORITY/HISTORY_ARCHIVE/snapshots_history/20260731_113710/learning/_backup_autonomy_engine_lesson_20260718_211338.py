from datetime import datetime

from learning.reasoning_engine import (
    reason,
    evaluate_reasoning,
)

from learning.planning_engine import build_plan
from learning.evaluation_engine import evaluate_plan
from learning.plan_feedback import generate_plan_feedback


def run_autonomy(context=None):
    """
    Controlled reasoning pipeline.

    observe
        -> reason
        -> evaluate reasoning
        -> build plan
        -> evaluate plan
        -> generate feedback

    Execution remains disabled.
    No system changes are performed.
    """

    context = context or {}

    # 1. REASON
    reasoning = reason(context)

    # 2. EVALUATE REASONING
    reasoning_evaluation = evaluate_reasoning(reasoning)

    # 3. BUILD PLAN
    plan = build_plan(reasoning)

    # 4. EVALUATE PLAN
    plan_evaluation = evaluate_plan(plan)

    # 5. GENERATE FEEDBACK
    feedback = generate_plan_feedback(
        plan,
        plan_evaluation,
    )

    return {
        "timestamp": str(datetime.now()),
        "reasoning": reasoning,
        "reasoning_evaluation": reasoning_evaluation,
        "plan": plan,
        "plan_evaluation": plan_evaluation,
        "feedback": feedback,
        "execution": "disabled",
        "status": "autonomy_pipeline_completed",
    }
