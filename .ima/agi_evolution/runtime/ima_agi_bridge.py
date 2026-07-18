from pathlib import Path
import json,time,subprocess,sys

ROOT=Path(".ima/agi_evolution/runtime")

def start_agi_layer():

    result={
        "time":time.time(),
        "status":"started",
        "layers":[]
    }

    jobs=[
        "ima_master_runtime.py",
        "decision_engine.py",
        "brain_controller.py"
    ]

    for job in jobs:
        try:
            out=subprocess.check_output(
                [sys.executable,str(ROOT/job)],
                text=True
            )

            result["layers"].append({
                "job":job,
                "status":"ok",
                "output":out[-200:]
            })

        except Exception as e:
            result["layers"].append({
                "job":job,
                "status":"failed",
                "error":str(e)
            })

    (ROOT/"agi_bridge_state.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)
    )

    return result



class IMA_AGI:
    def __init__(self):
        self.name="IMA_AGI_BRIDGE"

    def start(self):
        return start_agi_layer()

    def run(self):
        return start_agi_layer()

    def process(self, message=None):
        result=start_agi_layer()
        result["message"]=message
        return result


if __name__=="__main__":
    print(start_agi_layer())
