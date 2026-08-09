from datetime import datetime


def build_plan(reasoning_result):
    """
    Converts reasoning output into explicit executable steps.
    """
    hypotheses = reasoning_result.get("hypotheses", [])

    steps = []

    for index, item in enumerate(hypotheses, 1):
        steps.append({
            "step": index,
            "action": item.get("hypothesis"),
            "source": item.get("observation"),
            "status": "planned"
        })

    return {
        "timestamp": str(datetime.now()),
        "steps": steps,
        "status": "planned"
    }
