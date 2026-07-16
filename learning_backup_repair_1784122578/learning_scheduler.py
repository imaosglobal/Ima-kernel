from learning.self_improvement import run_self_improvement
from learning.ima_awareness import ima_awareness
from learning.gap_analyzer import analyze_gaps


def learning_cycle():

    awareness = ima_awareness()

    gaps = analyze_gaps()

    new_improvements = run_self_improvement()

    return {
        "awareness": awareness,
        "knowledge_gaps": gaps,
        "new_improvements": new_improvements,
        "status": "learning_cycle_completed"
    }
