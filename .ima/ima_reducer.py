import json

def reduce(events):
    state = {
        "files": set(),
        "mode": "INIT"
    }

    for e in events:
        t = e.get("type")
        d = e.get("data", {})

        if t == "FILE_ADD":
            state["files"].add(d.get("path"))

        elif t == "FILE_DELETE":
            state["files"].discard(d.get("path"))

        elif t == "KERNEL_REBUILD":
            state["mode"] = "REBUILT"

    state["files"] = list(state["files"])
    return state
