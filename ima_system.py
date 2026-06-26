import json, time, os, subprocess
from ima_brain import answer

LEDGER = ".ima/ledger.jsonl"


def emit(event_type, **data):
    os.makedirs(".ima", exist_ok=True)
    event = {"ts": time.time(), "type": event_type, "data": data}

    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\n")


def load_events():
    if not os.path.exists(LEDGER):
        return []
    return [json.loads(l) for l in open(LEDGER) if l.strip()]


def git_snapshot():
    subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return

    subprocess.run(["git", "commit", "-m", f"auto {int(time.time())}"])


# -------------------------
# QUESTION PIPELINE
# -------------------------
def ask(q):
    events = load_events()

    emit("QUESTION", text=q)

    response = answer(q, events)

    emit("ANSWER", text=response)

    print(response)
    git_snapshot()


def status():
    events = load_events()
    print("EVENTS:", len(events))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "ask":
        ask(" ".join(sys.argv[2:]))
    else:
        status()
