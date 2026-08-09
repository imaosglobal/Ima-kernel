from founder.executive_ai.continuous_intelligence.world_learning_bridge import collect_world_learning
from founder.executive_ai.self_learning_core.continuous_learning_loop import run_learning_cycle
from founder.executive_ai.evolution_core.policy_memory import save_rule
from founder.executive_ai.unified_brain.brain_state import update_state

def run():

    state={
        "world":collect_world_learning(),
        "learning":run_learning_cycle()
    }

    update_state(state)

    save_rule({
        "event":"master_cycle"
    })

    return state
