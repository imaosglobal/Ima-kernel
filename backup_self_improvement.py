from learning.improvement_engine import generate_improvements
from learning.self_reflection import suggest_improvement


def run_self_improvement():

    improvements = generate_improvements()

    for item in improvements:
        suggest_improvement(
            "self_learning",
            item
        )

    return improvements
