from pathlib import Path
import json
import time

import sys
from pathlib import Path

ROOT=Path(".ima/agi_evolution").resolve()
sys.path.insert(0,str(ROOT))

from evaluation.evaluate import run

def cycle():

    status=run()

    log={
        "time":time.time(),
        "status":status
    }

    Path(".ima/agi_evolution/runtime/evolution_log.jsonl").open(
        "a"
    ).write(json.dumps(log)+"\n")

    return status


if __name__=="__main__":
    print(cycle())
