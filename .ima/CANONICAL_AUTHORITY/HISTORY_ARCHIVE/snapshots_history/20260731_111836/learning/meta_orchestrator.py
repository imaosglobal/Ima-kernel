from learning.autonomy_engine import run_autonomy
from learning.system_introspection import *
from learning.learning_evaluator import evaluate_learning
from learning.suggest_improvements import suggest_improvements
from learning.capability_map import build_capability_map
from learning.health_check import health_report
from learning.improvement_planner import build_improvement_plan
from learning.decision_engine import make_learning_decision
from learning.feedback_planner import generate_feedback_improvements


def run_meta_analysis():

    autonomy = run_autonomy({
        "observations": [
            "meta analysis cycle started"
        ],
        "goals": [
            "improve system capability safely"
        ],
        "constraints": [
            "no autonomous execution",
            "planning only"
        ]
    })


    learning_state = evaluate_learning()

    capabilities = build_capability_map()
    health = health_report()
    suggestions = suggest_improvements()

    suggestion_texts = [
        x.get("suggestion","")
        if isinstance(x, dict)
        else str(x)
        for x in suggestions.get("suggestions",[])
    ]

    improvement_plan = build_improvement_plan(
        suggestion_texts
    )

    feedback_plan = generate_feedback_improvements()

    for item in improvement_plan:
        make_learning_decision(
            "system_improvement",
            item["suggestion"]
        )

    return {
        "capabilities": len(capabilities),
        "health_modules": len(health),
        "failed_health": [
            x for x in health
            if x["status"] != "ok"
        ],
        "suggestions": suggestions["suggestions"],
        "improvement_plan": improvement_plan,
        "feedback_plan": feedback_plan,
        "learning_state": learning_state,
        "autonomy": autonomy,
        "status": "meta_analysis_completed"
    }
