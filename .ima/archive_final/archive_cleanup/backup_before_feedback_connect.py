from learning.system_introspection import suggest_improvements
from learning.capability_map import build_capability_map
from learning.health_check import health_report
from learning.improvement_planner import build_improvement_plan
from learning.decision_engine import make_learning_decision


def run_meta_analysis():

    capabilities = build_capability_map()
    health = health_report()
    suggestions = suggest_improvements()

    improvement_plan = build_improvement_plan(
        suggestions["suggestions"]
    )

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
        "status": "meta_analysis_completed"
    }
