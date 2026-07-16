from pathlib import Path
import json
import time

ROOT=Path(".ima/agi_evolution")

REGISTRY=ROOT/"runtime/module_registry.json"


class IntegrationEngine:

    def __init__(self):
        if not REGISTRY.exists():
            REGISTRY.write_text("{}")


    def discover(self):

        modules=[]

        for f in ROOT.rglob("*_engine.py"):

            modules.append({
                "name":f.stem,
                "path":str(f),
                "time":time.time()
            })

        return modules


    def integrate(self):

        modules=self.discover()

        registry={
            "updated":time.time(),
            "modules":modules
        }

        REGISTRY.write_text(
            json.dumps(
                registry,
                indent=2,
                ensure_ascii=False
            )
        )

        return registry


if __name__=="__main__":
    print(
        json.dumps(
            IntegrationEngine().integrate(),
            indent=2,
            ensure_ascii=False
        )
    )
