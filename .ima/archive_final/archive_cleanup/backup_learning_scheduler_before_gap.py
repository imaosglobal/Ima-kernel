from learning.self_improvement import run_self_improvement
from learning.ima_awareness import ima_awareness


def learning_cycle():

    awareness = ima_awareness()

    new_improvements = run_self_improvement()

    return {
        "awareness": awareness,
        "new_improvements": new_improvements,
        "status": "learning_cycle_completed"
    }
