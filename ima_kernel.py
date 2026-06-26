#!/usr/bin/env python3
import os, json, time, subprocess, threading

# -------------------------
# STORAGE
# -------------------------
BASE = ".ima"
LEDGER = f"{BASE}/ledger.jsonl"
os.makedirs(BASE, exist_ok=True)


# -------------------------
# EVENT SYSTEM
# -------------------------
def emit(event_type, **data):
    event = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }
    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event


def load_events():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return [json.loads(l) for l in f if l.strip()]


# -------------------------
# QGE (QUESTION → ANSWER SPACE)
# -------------------------
def answer_space(q):
    return {
        "hypotheses": [
            {"answer": f"נראה ש־{q}", "score": 0.7},
            {"answer": "תהליך פנימי של עיבוד מידע", "score": 0.6},
            {"answer": "לא ידוע במדויק", "score": 0.3}
        ]
    }


def ask(question):
    qid = str(int(time.time() * 1000))

    emit("QUESTION", id=qid, text=question)

    result = {
        "id": qid,
        "text": f"תודעה היא חוויה פנימית של קיום, זיכרון ופרשנות של העולם.",
        "confidence": 0.9,
        "answers": answer_space(question)
    }

    emit("ANSWER", id=qid, text=result["text"])

    return result


# -------------------------
# GIT SNAPSHOT
# -------------------------
def git_snapshot():
    subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL)

    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return "NO_CHANGES"

    stamp = str(int(time.time()))
    subprocess.run(["git", "commit", "-m", f"auto snapshot {stamp}"])
    return stamp


# -------------------------
# REDUCER
# -------------------------
def reduce(events):
    state = {"questions": 0, "answers": 0, "files": set()}

    for e in events:
        if e["type"] == "QUESTION":
            state["questions"] += 1
        if e["type"] == "ANSWER":
            state["answers"] += 1

    state["files"] = list(state["files"])
    return state


# -------------------------
# DAEMON (FIXED)
# -------------------------
def daemon(interval=0.5):
    print("[IMA DAEMON] started")

    last_len = 0

    while True:
        try:
            events = load_events()

            if len(events) != last_len:
                last_len = len(events)

                print("[IMA DAEMON] event update:", last_len)

                # process only new QUESTIONS safely
                for e in events[-10:]:
                    if e.get("type") == "QUESTION":
                        q = e["data"]["text"]

                        result = ask(q)

                        if result:
                            emit("ANSWER", id=result["id"], text=result["text"])

                git_snapshot()

            time.sleep(interval)

        except KeyboardInterrupt:
            print("[IMA DAEMON] stopped")
            break


# -------------------------
# STATUS
# -------------------------
def status():
    events = load_events()
    state = reduce(events)

    print("=== IMA CLEAN KERNEL ===")
    print("EVENTS:", len(events))
    print("QUESTIONS:", state["questions"])
    print("ANSWERS:", state["answers"])


# -------------------------
# CLI
# -------------------------
def main():
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "ask":
        print(ask(" ".join(sys.argv[2:])))
    elif cmd == "emit":
        emit(sys.argv[2], text=" ".join(sys.argv[3:]))
    elif cmd == "daemon":
        daemon()
    else:
        status()


if __name__ == "__main__":
    main()
