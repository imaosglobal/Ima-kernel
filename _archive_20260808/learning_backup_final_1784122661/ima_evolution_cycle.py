from learning.meta_orchestrator import run_meta_analysis
from learning.health_check import health_report
from learning.system_improvement_memory import summarize_improvements


def run_evolution_cycle():

    print("=== IMA EVOLUTION CYCLE ===")

    health = health_report()

    failed = [
        x for x in health
        if x["status"] != "ok"
    ]

    print("HEALTH FAILED:", len(failed))

    meta = run_meta_analysis()

    print("CAPABILITIES:", meta["capabilities"])
    print("SUGGESTIONS:", len(meta["suggestions"]))

    print()
    print("SYSTEM HISTORY:")
    print(summarize_improvements())


if __name__ == "__main__":
    run_evolution_cycle()
