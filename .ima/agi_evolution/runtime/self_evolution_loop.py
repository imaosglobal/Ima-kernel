from pathlib import Path
import json
import time

ROOT=Path(".ima/agi_evolution")


class SelfEvolutionLoop:

    def __init__(self):
        self.capability_file=ROOT/"AGI_MASTER_GAP_MAP.json"
        self.plan_file=ROOT/"runtime/evolution_plan.json"


    def load_capabilities(self):
        if self.capability_file.exists():
            return json.loads(
                self.capability_file.read_text()
            )
        return {}


    def analyze(self):
        data=self.load_capabilities()

        missing=[]

        for name,value in data.get(
            "missing_capabilities",{}
        ).items():

            if value.get("status") in [
                "missing",
                "partial"
            ]:
                missing.append({
                    "capability":name,
                    "goal":value.get("goal")
                })

        return missing


    def create_plan(self):

        gaps=self.analyze()

        priority=[
            x["capability"]
            for x in gaps
        ]

        plan={
            "time":time.time(),
            "detected_gaps":gaps,
            "priority_order":priority,
            "next_action":
                "create_module_proposal"
        }

        self.plan_file.write_text(
            json.dumps(
                plan,
                indent=2,
                ensure_ascii=False
            )
        )

        return plan


IMA_SELF_EVOLUTION=SelfEvolutionLoop()


if __name__=="__main__":
    print(json.dumps(
        IMA_SELF_EVOLUTION.create_plan(),
        indent=2,
        ensure_ascii=False
    ))
