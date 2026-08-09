from founder.executive_ai.action_engine.action_orchestrator import run_world_actions
from founder.executive_ai.action_engine.action_learning_loop import learning_cycle


def run_cycle():

    print("=== IMA AUTONOMOUS CYCLE START ===")

    actions = run_world_actions()

    learning = learning_cycle()

    return {
        "actions": actions,
        "learning": learning,
        "status": "cycle_completed"
    }


if __name__ == "__main__":

    result = run_cycle()

    print(result)
