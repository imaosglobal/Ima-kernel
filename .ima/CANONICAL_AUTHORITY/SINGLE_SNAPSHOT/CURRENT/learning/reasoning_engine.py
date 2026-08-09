from datetime import datetime


def reason(context):
    """
    Minimal deterministic reasoning layer.
    Produces explicit observations, hypotheses, constraints and next steps.
    """
    context = context or {}

    observations = context.get("observations", [])
    goals = context.get("goals", [])
    constraints = context.get("constraints", [])

    if not isinstance(observations, list):
        observations = [observations]

    if not isinstance(goals, list):
        goals = [goals]

    if not isinstance(constraints, list):
        constraints = [constraints]

    hypotheses = []

    for observation in observations:
        if observation:
            hypotheses.append({
                "observation": observation,
                "hypothesis": f"Investigate: {observation}",
                "confidence": 0.5
            })

    return {
        "timestamp": str(datetime.now()),
        "observations": observations,
        "goals": goals,
        "constraints": constraints,
        "hypotheses": hypotheses,
        "status": "reasoned"
    }


def evaluate_reasoning(result):
    return {
        "valid": isinstance(result, dict),
        "has_observations": bool(result.get("observations")),
        "has_hypotheses": bool(result.get("hypotheses")),
        "status": "evaluated"
    }
