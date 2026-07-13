import json

CORE = __import__("ima.runtime.core", fromlist=["*"])

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
