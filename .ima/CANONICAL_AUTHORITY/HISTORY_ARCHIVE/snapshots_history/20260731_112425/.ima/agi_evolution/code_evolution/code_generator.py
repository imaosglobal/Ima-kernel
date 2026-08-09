from pathlib import Path
import json
import time

ROOT=Path(".ima/agi_evolution")

class CodeGenerator:

    def generate(self,capability):
        folder=ROOT/capability
        folder.mkdir(parents=True,exist_ok=True)

        file=folder/f"{capability}_engine.py"

        if file.exists():
            return {
                "status":"exists",
                "file":str(file)
            }

        code=f'''
from pathlib import Path
import time

class {capability.title().replace("_","")}Engine:

    def __init__(self):
        self.name="{capability}"

    def status(self):
        return {{
            "capability":self.name,
            "time":time.time(),
            "status":"online"
        }}

ENGINE={capability.title().replace("_","")}Engine()
'''

        file.write_text(code)

        return {
            "status":"created",
            "file":str(file)
        }


GENERATOR=CodeGenerator()


if __name__=="__main__":
    print(GENERATOR.generate("adaptive_identity"))
