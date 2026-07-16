from pathlib import Path
import json
import time

ROOT=Path(".ima/agi_evolution")

class BuilderEngine:

    def __init__(self):
        self.plan=ROOT/"runtime/evolution_plan.json"
        self.output=ROOT/"code_evolution/proposals"


    def load_plan(self):
        if self.plan.exists():
            return json.loads(self.plan.read_text())
        return {}


    def create_proposals(self):

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

        plan=self.load_plan()

        proposals=[]

        for item in plan.get(
            "detected_gaps",[]
        ):

            name=item["capability"]

            proposal={
                "capability":name,
                "goal":item["goal"],
                "created":time.time(),
                "status":"proposal",
                "files_to_create":[
                    f"{name}/{name}_engine.py"
                ],
                "requires_test":True
            }

            path=self.output/f"{name}_proposal.json"

            path.write_text(
                json.dumps(
                    proposal,
                    indent=2,
                    ensure_ascii=False
                )
            )

            proposals.append(proposal)


        return proposals


BUILDER=BuilderEngine()


if __name__=="__main__":
    print(json.dumps(
        BUILDER.create_proposals(),
        indent=2,
        ensure_ascii=False
    ))
