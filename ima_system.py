import json, time, os, subprocess

LEDGER = ".ima/ledger.jsonl"


# ---------------------------
# EVENT BUS
# ---------------------------
def emit(event_type, **data):
    os.makedirs(".ima", exist_ok=True)

    event = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }

    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\n")


def load_events():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(l) for l in f if l.strip()]


# ---------------------------
# REDUCER (STATE BUILD)
# ---------------------------
def reduce(events):
    state = {
        "files": set(),
        "mode": "INIT"
    }

    for e in events:
        t = e["type"]
        d = e.get("data", {})

        if t == "FILE_ADD":
            state["files"].add(d.get("path"))

        elif t == "FILE_REMOVE":
            state["files"].discard(d.get("path"))

        elif t == "KERNEL_RESET":
            state["mode"] = "RESET"

    state["files"] = sorted(list(state["files"]))
    return state


# ---------------------------
# GIT SNAPSHOT ENGINE
# ---------------------------
def git_snapshot():
    subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL)

    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return "NO_CHANGES"

    stamp = str(int(time.time()))
    subprocess.run(["git", "commit", "-m", f"snapshot {stamp}"])
    return stamp


# ---------------------------
# STATE BUILDER
# ---------------------------
def build_state():
    events = load_events()
    return reduce(events)


# ---------------------------
# SYSTEM STATUS
# ---------------------------
def status():
    state = build_state()

    print("=== IMA UNIFIED KERNEL ===")
    print("FILES:", len(state["files"]))
    print("MODE:", state["mode"])


# ---------------------------
# COMMANDS
# ---------------------------
def run():
    cmd = os.sys.argv[1] if len(os.sys.argv) > 1 else "status"

    if cmd == "emit":
        emit(os.sys.argv[2], path=os.sys.argv[3])
        return

    if cmd == "snapshot":
        print(git_snapshot())
        return

    if cmd == "status":
        status()
        return


if __name__ == "__main__":
    run()
