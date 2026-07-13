from learning.meta_orchestrator import run_meta_analysis
from learning.ima_learning_loop import run_ima_learning_loop


def run_safe_cycle():
    meta = run_meta_analysis()

    cycle = run_ima_learning_loop()

    return {
        "meta_status": meta.get("status"),
        "cycle_status": cycle.get("status"),
        "suggestions": meta.get("suggestions", []),
        "feedback": cycle.get("feedback_cycle", []),
        "status": "safe_cycle_completed"
    }
