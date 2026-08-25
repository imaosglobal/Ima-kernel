import subprocess
from pathlib import Path
import json

ROOT=Path(__file__).parent

def boot_runtime():
    result=subprocess.check_output(
        ["node",str(ROOT/"IMA_RUNTIME.js")],
        text=True
    )
    return json.loads(result)

if __name__=="__main__":
    print(boot_runtime())
