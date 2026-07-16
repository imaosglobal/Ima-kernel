from pathlib import Path
import json
import time

ROOT=Path(".ima/agi_evolution/code_evolution/proposals")

class ValidatorEngine:

    def validate(self):

        results=[]

        for file in ROOT.glob("*_proposal.json"):

            data=json.loads(file.read_text())

            result={
                "capability":data["capability"],
                "time":time.time(),
                "checks":{
                    "proposal_exists":True,
                    "goal_defined":bool(data.get("goal")),
                    "requires_test":data.get("requires_test",False)
                },
                "status":"approved"
            }

            results.append(result)

        Path(
            ".ima/agi_evolution/runtime/validation_report.json"
        ).write_text(
            json.dumps(
                results,
                indent=2,
                ensure_ascii=False
            )
        )

        return results


VALIDATOR=ValidatorEngine()


if __name__=="__main__":
    print(json.dumps(
        VALIDATOR.validate(),
        indent=2,
        ensure_ascii=False
    ))
