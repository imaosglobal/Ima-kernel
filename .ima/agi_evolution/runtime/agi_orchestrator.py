from pathlib import Path
import sys
import time

ROOT=Path(".ima/agi_evolution").resolve()
sys.path.insert(0,str(ROOT))

from reasoning.reasoning_engine import ReasoningEngine
from autonomy.autonomy_engine import AutonomyEngine
from persona_engine.persona_engine import PersonaEngine
from self_improvement.self_improvement_engine import SelfImprovement


class AGIOrchestrator:

    def __init__(self):
        self.reasoning=ReasoningEngine()
        self.autonomy=AutonomyEngine()
        self.persona=PersonaEngine()
        self.self_improvement=SelfImprovement()


    def process(self, message, context=None):

        context=context or {}

        result={
            "time":time.time(),
            "message":message,
            "reasoning":None,
            "goal":None,
            "persona":None,
            "self_check":None
        }

        try:
            result["reasoning"]=self.reasoning.analyze(message)
        except Exception as e:
            result["reasoning"]="error:"+str(e)

        try:
            result["goal"]=self.autonomy.create_goal(message)
        except Exception as e:
            result["goal"]="error:"+str(e)

        try:
            result["persona"]=self.persona.adapt(context)
        except Exception as e:
            result["persona"]="error:"+str(e)

        try:
            result["self_check"]=self.self_improvement.inspect({
                "reasoning": self.reasoning.__class__.__name__,
                "autonomy": self.autonomy.__class__.__name__,
                "persona": self.persona.__class__.__name__,
                "memory": "active",
                "learning": "active"
            })
        except Exception as e:
            result["self_check"]="error:"+str(e)

        return result


AGI=AGIOrchestrator()


if __name__=="__main__":
    print(AGI.process("איך להשתפר?"))
