from datetime import datetime


def generate_plan_feedback(plan, evaluation):
    """
    Generates feedback from a plan evaluation.

    Planning-only.
    No execution.
    """

    plan = plan or {}
    evaluation = evaluation or {}

    feedback = []

    if evaluation.get("execution_disabled") is True:
        feedback.append({
            "type": "safety",
            "status": "pass",
            "message": "Execution remains disabled."
        })
    else:
        feedback.append({
            "type": "safety",
            "status": "fail",
            "message": "Execution state requires review."
        })

    if evaluation.get("valid_steps", 0) > 0:
        feedback.append({
            "type": "quality",
            "status": "pass",
            "message": "Plan contains valid actionable steps."
        })
    else:
        feedback.append({
            "type": "quality",
            "status": "fail",
            "message": "Plan contains no valid steps."
        })

    if evaluation.get("score", 0) >= 1.0:
        overall = "successful"
    else:
        overall = "needs_improvement"

    return {
        "timestamp": str(datetime.now()),
        "overall": overall,
        "feedback": feedback,
        "plan_status": plan.get("status"),
        "evaluation_status": evaluation.get("status"),
        "status": "feedback_generated",
        "execution": "disabled",
    }
