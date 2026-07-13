from learning.system_introspection import suggest_improvements
from learning.capability_map import build_capability_map
from learning.health_check import health_report


def run_meta_analysis():

    capabilities = build_capability_map()
    health = health_report()
    suggestions = suggest_improvements()

    return {
        "capabilities": len(capabilities),
        "health_modules": len(health),
        "failed_health": [
            x for x in health
            if x["status"] != "ok"
        ],
        "suggestions": suggestions["suggestions"],
        "status": "meta_analysis_completed"
    }
