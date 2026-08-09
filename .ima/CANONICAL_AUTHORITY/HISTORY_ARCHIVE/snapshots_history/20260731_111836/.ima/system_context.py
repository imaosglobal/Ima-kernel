
import json
from pathlib import Path

DECISION=Path(".ima/decision_memory.py")

def get_system_context():

    try:
        import importlib.util

        spec=importlib.util.spec_from_file_location(
            "decision_memory",
            DECISION
        )

        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        return mod.context()

    except Exception as e:
        return {
            "error":str(e),
            "rules":[]
        }


if __name__=="__main__":
    print(json.dumps(
        get_system_context(),
        ensure_ascii=False,
        indent=2
    ))
