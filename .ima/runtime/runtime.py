import json

import importlib.util
spec = importlib.util.spec_from_file_location("ima_core", ".ima/runtime/core.py")
CORE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CORE)

def load_patches():
    try:
        return [json.loads(l) for l in open(".ima/runtime/patches.jsonl")]
    except:
        return []

def apply_patches():
    patches = load_patches()

    for p in patches:
        if p["target"] == "score":
            # future: inject logic safely
            pass

    return CORE

RUNTIME = apply_patches()

if __name__ == "__main__":
    import sys
    RUNTIME.ask(" ".join(sys.argv[1:]))
