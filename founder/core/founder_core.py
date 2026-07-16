from founder.executive_ai.memory.memory_bridge import enrich_answer
from founder.executive_ai.advisor.founder_advisor import advise
from founder.executive_ai.action_engine.action_orchestrator import run_world_actions


class FounderCore:

    def __init__(self):
        self.name="IMA Founder Core"

    def think(self):
        memory = enrich_answer('founder_cycle', [])
        advice = advise(memory)

        return {
            "memory": memory,
            "advice": advice
        }

    def act(self):
        return run_world_actions()

    def cycle(self):
        decision = self.think()
        actions = self.act()

        return {
            "decision": decision,
            "actions": actions
        }


def run_founder_cycle():
    core=FounderCore()
    return core.cycle()
