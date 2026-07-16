from pathlib import Path
import json
import time
import sys

ROOT=Path(".ima/agi_evolution")

sys.path.insert(0,str(ROOT/"code_evolution"))

from code_generator import GENERATOR


class AutoBuilder:

    def __init__(self):
        self.plan=ROOT/"runtime/evolution_plan.json"

    def run(self):

        if not self.plan.exists():
            return {"status":"no_plan"}

        data=json.loads(self.plan.read_text())

        results=[]

        for item in data.get("detected_gaps",[]):

            capability=item["capability"]

            result=GENERATOR.generate(capability)

            results.append({
                "capability":capability,
                "result":result,
                "time":time.time()
            })

        out=ROOT/"runtime/autobuild_result.json"

        out.write_text(
            json.dumps(
                results,
                indent=2,
                ensure_ascii=False
            )
        )

        return results


if __name__=="__main__":
    print(
        json.dumps(
            AutoBuilder().run(),
            indent=2,
            ensure_ascii=False
        )
    )
