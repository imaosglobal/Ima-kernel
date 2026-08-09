
from pathlib import Path
import json,time
import importlib.util

CHECK=Path(".ima/self_check.py")
LOG=Path(".ima/system_supervisor_log.jsonl")

def run_check():

    spec=importlib.util.spec_from_file_location(
        "self_check",
        CHECK
    )

    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result=mod.check()

    event={
        "time":time.time(),
        "type":"SYSTEM_CHECK",
        "healthy":result.get("system_ready",False),
        "rules":result.get("learning_rules",0)
    }

    with LOG.open("a",encoding="utf-8") as f:
        f.write(json.dumps(event,ensure_ascii=False)+"\n")

    return event


if __name__=="__main__":
    print(json.dumps(
        run_check(),
        ensure_ascii=False,
        indent=2
    ))
