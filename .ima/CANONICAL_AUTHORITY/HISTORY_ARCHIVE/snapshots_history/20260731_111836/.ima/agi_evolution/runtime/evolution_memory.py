from pathlib import Path
import json,time

FILE=Path(".ima/agi_evolution/runtime/evolution_history.json")

class EvolutionMemory:

    def __init__(self):
        if not FILE.exists():
            FILE.write_text("[]")

    def record(self,event):
        data=json.loads(FILE.read_text())
        data.append({
            "time":time.time(),
            "event":event
        })
        FILE.write_text(json.dumps(data,indent=2,ensure_ascii=False))

    def history(self):
        return json.loads(FILE.read_text())

MEMORY=EvolutionMemory()

if __name__=="__main__":
    MEMORY.record("evolution memory online")
    print(MEMORY.history()[-1])
