from learning.state_transition_learner import learn
from learning.state_transition_outcome import evaluate_all


def run_state_transition_learning():
    model = learn()
    evaluation = evaluate_all()

    return {
        "status": "ok",
        "model": model,
        "evaluation": evaluation,
    }


if __name__ == "__main__":
    result = run_state_transition_learning()

    print("=" * 72)
    print("IMA STATE TRANSITION LEARNING SERVICE")
    print("=" * 72)

    print("STATUS:", result["status"])
    print("EVENTS:", result["evaluation"]["events"])
    print("EVALUATED:", result["evaluation"]["evaluated"])
    print("ACCURACY:", result["evaluation"]["accuracy"])

    print("=" * 72)
