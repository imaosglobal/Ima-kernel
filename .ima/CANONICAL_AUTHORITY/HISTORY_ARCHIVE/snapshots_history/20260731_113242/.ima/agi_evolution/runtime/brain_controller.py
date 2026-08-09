import subprocess,sys,json,time
from pathlib import Path

ROOT=Path(".ima/agi_evolution/runtime")

def run():

    jobs=[
        "continuity_engine.py",
        "repair_engine.py",
        "goal_engine.py"
    ]

    result={
        "time":time.time(),
        "steps":[]
    }

    for job in jobs:
        try:
            out=subprocess.check_output(
                [sys.executable,str(ROOT/job)],
                text=True
            )

            result["steps"].append({
                "job":job,
                "status":"ok",
                "output":out[-300:]
            })

        except Exception as e:
            result["steps"].append({
                "job":job,
                "status":"failed",
                "error":str(e)
            })

    (ROOT/"brain_state.json").write_text(
        json.dumps(result,indent=2)
    )

    return result


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
