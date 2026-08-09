
from pathlib import Path
import importlib.util

CTX=Path(".ima/system_context.py")

def load_awareness():

    try:
        spec=importlib.util.spec_from_file_location(
            "system_context",
            CTX
        )

        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        return mod.get_system_context()

    except Exception:
        return {
            "rules":[],
            "lessons_count":0
        }


def apply_context(result):

    result["system_awareness"]=load_awareness()

    return result
