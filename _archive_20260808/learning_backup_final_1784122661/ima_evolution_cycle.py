from learning.meta_orchestrator import run_meta_analysis
from learning.health_check import health_report
from learning.system_improvement_memory import summarize_improvements


def run_evolution_cycle():


    health = health_report()

    failed = [
        x for x in health
        if x["status"] != "ok"
    ]


    meta = run_meta_analysis()




if __name__ == "__main__":
    run_evolution_cycle()
