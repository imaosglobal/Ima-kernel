from learning.learning_memory import load_memory, save_memory
from datetime import datetime


def evaluate_action(action, result, score):

    data = load_memory()

    data.setdefault("evaluations", [])

    data["evaluations"].append({
        "time": str(datetime.now()),
        "action": action,
        "result": result,
        "score": score
    })

    save_memory(data)

    return {
        "action": action,
        "score": score,
        "status": "evaluated"
    }


def get_evaluations():

    data = load_memory()

    return data.get("evaluations", [])


def evaluate_plan(plan):
    """
    Evaluates a plan without executing it.

    Planning-only evaluation:
    - validates structure
    - counts steps
    - checks that execution is not requested
    """

    plan = plan or {}
    steps = plan.get("steps", [])

    if not isinstance(steps, list):
        steps = []

    valid_steps = [
        step for step in steps
        if isinstance(step, dict)
        and step.get("action")
    ]

    execution_disabled = all(
        step.get("status") == "planned"
        for step in valid_steps
    )

    score = 1.0 if execution_disabled else 0.0

    result = {
        "plan_status": plan.get("status"),
        "step_count": len(steps),
        "valid_steps": len(valid_steps),
        "execution_disabled": execution_disabled,
        "score": score,
        "status": "plan_evaluated",
        "timestamp": str(datetime.now()),
    }

    return result
