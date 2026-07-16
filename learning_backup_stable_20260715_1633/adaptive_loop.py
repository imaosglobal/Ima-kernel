from learning.feedback_engine import process_feedback
from learning.learning_memory import store_pattern


def run_adaptive_cycle():

    feedback = process_feedback()

    for item in feedback:
        store_pattern(
            f"feedback_pattern:{item}"
        )

    return {
        "feedback": feedback,
        "status": "adaptive_cycle_completed"
    }
