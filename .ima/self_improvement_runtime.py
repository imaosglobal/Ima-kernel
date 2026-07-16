
from pathlib import Path
import json,time

ENGINE=Path(".ima/self_improvement_engine.json")
LESSONS=Path(".ima/system_learning.jsonl")

def load_engine():
    if not ENGINE.exists():
        return {}
    return json.loads(ENGINE.read_text(encoding="utf-8"))

def observe():
    data={
        "time":time.time(),
        "type":"SELF_CHECK",
        "checks":{
            "engine":ENGINE.exists(),
            "lessons":LESSONS.exists()
        }
    }
    return data

def learn(lesson):
    with LESSONS.open("a",encoding="utf-8") as f:
        f.write(json.dumps(
            lesson,
            ensure_ascii=False
        )+"\n")

def run():
    engine=load_engine()
    result=observe()

    if result["checks"]["engine"]:
        learn({
            "type":"SYSTEM_LEARNING",
            "time":time.time(),
            "lesson":"self improvement runtime connected",
            "details":{
                "pipeline":engine.get("pipeline",[])
            }
        })

    return result

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2))
