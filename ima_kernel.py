#!/usr/bin/env python3
import os, json, time, subprocess, threading

# -------------------------
# PATHS
# -------------------------
BASE = ".ima"
LEDGER = f"{BASE}/ledger.jsonl"
PID_FILE = f"{BASE}/daemon.pid"
LOCK_FILE = f"{BASE}/git.lock"

os.makedirs(BASE, exist_ok=True)


# -------------------------
# SAFE UTIL
# -------------------------
def now():
    return int(time.time())


def write_jsonl(path, obj):
    with open(path, "a") as f:
        f.write(json.dumps(obj) + "\n")


def read_events():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(l) for l in f if l.strip()]


# -------------------------
# EVENT BUS (stable)
# -------------------------
def emit(event_type, **data):
    e = {"ts": now(), "type": event_type, "data": data}
    write_jsonl(LEDGER, e)
    return e


# -------------------------
# CORE ANSWER ENGINE (stable)
# -------------------------
def ask(q):
    qid = str(now())

    emit("QUESTION", id=qid, text=q)

    result = {
        "id": qid,
        "text": "תודעה היא מערכת של חוויה, עיבוד מידע וזיכרון מתמשך.",
        "confidence": 0.9
    }

    emit("ANSWER", id=qid, text=result["text"])
    return result


# -------------------------
# REDUCER
# -------------------------
def reduce(events):
    return {
        "questions": sum(1 for e in events if e["type"] == "QUESTION"),
        "answers": sum(1 for e in events if e["type"] == "ANSWER")
    }


# -------------------------
# GIT CONTROL (FIXED)
# -------------------------
_last_git = 0
GIT_INTERVAL = 10  # seconds throttle


def git_snapshot():
    global _last_git

    if now() - _last_git < GIT_INTERVAL:
        return "THROTTLED"

    _last_git = now()

    # prevent concurrent git
    if os.path.exists(LOCK_FILE):
        return "LOCKED"

    try:
        open(LOCK_FILE, "w").write("1")

        subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL)

        r = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if r.returncode == 0:
            return "NO_CHANGES"

        subprocess.run(
            ["git", "commit", "-m", f"auto snapshot {now()}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return "COMMITTED"

    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)


# -------------------------
# DAEMON (FIXED: SAFE LOOP)
# -------------------------
def daemon(interval=1.5):
    print("[IMA DAEMON] started")

    last_index = 0
    queue = []

    events = read_events()
    last_index = len(events)

    while True:
        try:
            events = read_events()
            new_events = events[last_index:]
            last_index = len(events)

            # push only new questions
            for e in new_events:
                if e["type"] == "QUESTION":
                    queue.append(e)

            # process limited batch (BACKPRESSURE)
            batch = queue[:3]
            queue = queue[3:]

            for q in batch:
                res = ask(q["data"]["text"])

            # git is throttled
            git_snapshot()

            time.sleep(interval)

        except KeyboardInterrupt:
            print("[IMA DAEMON] stopped")
            break


# -------------------------
# STATUS
# -------------------------
def status():
    events = read_events()
    stats = reduce(events)

    print("=== IMA STABLE KERNEL ===")
    print("EVENTS:", len(events))
    print("QUESTIONS:", stats["questions"])
    print("ANSWERS:", stats["answers"])


# -------------------------
# CLI
# -------------------------
def main():
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "ask":
        print(ask(" ".join(sys.argv[2:])))
    elif cmd == "daemon":
        daemon()
    elif cmd == "status":
        status()
    else:
        status()


if __name__ == "__main__":
    main()
