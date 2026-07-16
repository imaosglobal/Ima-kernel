from pathlib import Path
import json
import time
import subprocess
import sys

ROOT=Path(".ima/agi_evolution")

class AutonomousEvolutionController:

    def __init__(self):
        self.state=ROOT/"runtime/autonomous_state.json"

    def run(self):

        result={
            "time":time.time(),
            "steps":[]
        }

        steps=[
            ("scan",
             ".ima/agi_evolution/runtime/evolution_manager.py"),

            ("plan",
             ".ima/agi_evolution/runtime/self_evolution_loop.py"),

            ("build",
             ".ima/agi_evolution/code_evolution/builder_engine.py"),

            ("validate",
             ".ima/agi_evolution/code_evolution/validator_engine.py"),

            ("cycle",
             ".ima/agi_evolution/runtime/evolution_cycle.py")
        ]

        for name,file in steps:
            try:
                out=subprocess.check_output(
                    [sys.executable,file],
                    stderr=subprocess.STDOUT,
                    text=True
                )

                result["steps"].append({
                    "step":name,
                    "status":"success",
                    "output":out[-500:]
                })

            except Exception as e:
                result["steps"].append({
                    "step":name,
                    "status":"failed",
                    "error":str(e)
                })


        self.state.write_text(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

        return result


IMA_AUTONOMOUS_EVOLUTION=AutonomousEvolutionController()


if __name__=="__main__":
    print(json.dumps(
        IMA_AUTONOMOUS_EVOLUTION.run(),
        indent=2,
        ensure_ascii=False
    ))
