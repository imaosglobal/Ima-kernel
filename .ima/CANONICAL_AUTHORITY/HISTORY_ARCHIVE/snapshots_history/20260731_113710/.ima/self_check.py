
import time
from pathlib import Path
import json

from importlib.util import spec_from_file_location, module_from_spec

BRIDGE=Path(".ima/ima_awareness_bridge.py")

def get_state():

    try:
        spec=spec_from_file_location(
            "bridge",
            BRIDGE
        )

        mod=module_from_spec(spec)
        spec.loader.exec_module(mod)

        return mod.load_awareness()

    except Exception as e:
        return {
            "error":str(e)
        }


def check():

    state=get_state()

    return {
        "time":time.time(),
        "system_ready": "rules" in state,
        "learning_rules":len(state.get("rules",[])),
        "state":state
    }


if __name__=="__main__":
    print(json.dumps(
        check(),
        ensure_ascii=False,
        indent=2
    ))
