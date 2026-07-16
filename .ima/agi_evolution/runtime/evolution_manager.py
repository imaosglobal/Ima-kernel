from pathlib import Path
import json
import time

ROOT=Path(".ima/agi_evolution")

class EvolutionManager:

    def __init__(self):
        self.registry=self.load_registry()

    def load_registry(self):
        p=ROOT/"runtime/evolution_os_registry.json"
        if p.exists():
            return json.loads(p.read_text())
        return {}

    def inspect(self):
        report={
            "time":time.time(),
            "systems":{}
        }

        for system in self.registry.get("systems",[]):
            path=ROOT/system
            report["systems"][system]={
                "exists":path.exists(),
                "files":len(list(path.rglob("*"))) if path.exists() else 0
            }

        return report


    def plan_upgrade(self):
        state=self.inspect()

        missing=[]

        for k,v in state["systems"].items():
            if not v["exists"]:
                missing.append(k)

        return {
            "time":time.time(),
            "missing":missing,
            "action":"expand_capabilities"
        }


IMA_EVOLUTION=EvolutionManager()


if __name__=="__main__":
    print(json.dumps(
        {
        "state":IMA_EVOLUTION.inspect(),
        "plan":IMA_EVOLUTION.plan_upgrade()
        },
        indent=2,
        ensure_ascii=False
    ))
