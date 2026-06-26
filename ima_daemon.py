#!/usr/bin/env python3

import time, json, os, subprocess

LEDGER = ".ima/ledger.jsonl"
STATE_FILE = ".ima/core_state.json"
PID_FILE = ".ima/daemon.pid"


# -------------------------
# LOAD EVENTS
# -------------------------
def load_events():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(l) for l in f if l.strip()]


# -------------------------
# REDUCER (QGE CORE)
# -------------------------
def reduce(events):
    nodes = set()
    edges = []

    for e in events:
        if e["type"] == "QUESTION":
            nodes.add(e["data"].get("text"))

        if e["type"] == "FILE_ADD":
            nodes.add(e["data"].get("path"))

    return {
        "nodes": list(nodes),
        "edges": edges,
        "event_count": len(events)
    }


# -------------------------
# BUILD STATE
# -------------------------
def build():
    events = load_events()
    state = reduce(events)

    os.makedirs(".ima", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    return state


# -------------------------
# GIT SYNC (OPTIONAL AUTO SNAPSHOT)
# -------------------------
def git_snapshot():
    subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL)

    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return

    subprocess.run([
        "git", "commit", "-m",
        f"auto-daemon-sync {int(time.time())}"
    ], stdout=subprocess.DEVNULL)


# -------------------------
# DAEMON LOOP
# -------------------------
def run_daemon(interval=1.0):
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    last_mtime = 0

    print("[IMA DAEMON] started")

    while True:
        try:
            if os.path.exists(LEDGER):
                mtime = os.path.getmtime(LEDGER)

                if mtime != last_mtime:
                    last_mtime = mtime

                    state = build()
                    print("[IMA DAEMON] event update:", state["event_count"])

                    git_snapshot()

            time.sleep(interval)

        except KeyboardInterrupt:
            print("[IMA DAEMON] stopped")
            break


# -------------------------
# ENTRY
# -------------------------
if __name__ == "__main__":
    run_daemon()
