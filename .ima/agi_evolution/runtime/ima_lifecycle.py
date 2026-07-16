import subprocess,sys,json,time
from pathlib import Path

ROOT=Path(".ima/agi_evolution/runtime")

JOBS=[
"ima_master_runtime.py",
"decision_engine.py",
"brain_controller.py",
        "cognitive_pipeline.py"
]

def run():

    result={
        "time":time.time(),
        "cycle":"started",
        "steps":[]
    }

    for j in JOBS:
        try:
            out=subprocess.check_output(
                [sys.executable,str(ROOT/j)],
                text=True
            )

            result["steps"].append({
                "job":j,
                "status":"ok",
                "output":out[-300:]
            })

        except Exception as e:
            result["steps"].append({
                "job":j,
                "status":"failed",
                "error":str(e)
            })

    (ROOT/"lifecycle_state.json").write_text(
        json.dumps(result,indent=2)
    )

    return result


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
