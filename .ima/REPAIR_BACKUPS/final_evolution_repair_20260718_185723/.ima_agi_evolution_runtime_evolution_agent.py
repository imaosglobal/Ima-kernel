from pathlib import Path
import json
import time
import shutil

ROOT=Path(".ima/agi_evolution")
BACKUP=ROOT/"governance/backups"

class EvolutionAgent:

    def __init__(self):
        BACKUP.mkdir(parents=True,exist_ok=True)

    def read_plan(self):
        p=ROOT/"runtime/evolution_plan.json"
        if p.exists():
            return json.loads(p.read_text())
        return {}

    def backup(self,path):
        src=Path(path)
        if src.exists():
            dst=BACKUP/(src.name+"."+str(int(time.time())))
            shutil.copy(src,dst)

    def create_module(self,capability):
        folder=ROOT/capability
        folder.mkdir(parents=True,exist_ok=True)

        file=folder/(capability+"_engine.py")

        if file.exists():
            return {
                "status":"exists",
                "file":str(file)
            }

        content=f'''
class {capability.title().replace("_","")}Engine:

    def __init__(self):
        self.name="{capability}"

    def inspect(self):
        return {{
            "capability":"{capability}",
            "status":"prototype"
        }}

    def improve(self,data=None):
        return {{
            "capability":"{capability}",
            "action":"improvement planned"
        }}
'''

        file.write_text(content)

        return {
            "status":"created",
            "file":str(file)
        }


    def evolve(self):

        plan=self.read_plan()
        results=[]

        for item in plan.get("detected_gaps",[]):

            cap=item["capability"]

            result=self.create_module(cap)

            results.append({
                "capability":cap,
                "result":result,
                "time":time.time()
            })


        report={
            "time":time.time(),
            "created":results,
            "status":"evolution_cycle_complete"
        }

        (ROOT/"runtime/evolution_result.json").write_text(
            json.dumps(report,indent=2,ensure_ascii=False)
        )

        return report


AGENT=EvolutionAgent()


if __name__=="__main__":
    print(json.dumps(
        AGENT.evolve(),
        indent=2,
        ensure_ascii=False
    ))
