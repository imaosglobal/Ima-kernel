import json, time, os, subprocess, sys

LEDGER = ".ima/ledger.jsonl"


# -------------------
# EVENT CORE
# -------------------
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


# -------------------
# REDUCER → GRAPH
# -------------------
def build_graph(events):
    nodes = set()
    edges = []

    last_q = None

    for e in events:
        t = e["type"]
        d = e.get("data", {})

        if t == "QUESTION":
            q = d.get("text")
            nodes.add(q)
            last_q = q

        if t == "ANSWER":
            a = d.get("answer")
            nodes.add(a)
            if last_q:
                edges.append((last_q, a))

    return {
        "nodes": list(nodes),
        "edges": edges
    }


# -------------------
# QGE CORE
# -------------------
def answer_space(q):
    return {
        "hypotheses": [
            {"answer": "A", "score": 0.5},
            {"answer": "B", "score": 0.3},
            {"answer": "UNKNOWN", "score": 0.2}
        ]
    }


def ask(question):
    qid = str(int(time.time()))

    emit("QUESTION", id=qid, text=question)

    expanded = [
        question,
        f"{question} (context)",
        f"{question} (check)",
        f"{question} (external)"
    ]

    answers = answer_space(question)

    # emit answers into graph
    for h in answers["hypotheses"]:
        emit("ANSWER", id=qid, answer=h["answer"], score=h["score"])

    return {
        "id": qid,
        "expanded": expanded,
        "answers": answers
    }


# -------------------
# GIT SYNC ENGINE
# -------------------
def git_snapshot():
    subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL)

    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return "NO_CHANGES"

    stamp = str(int(time.time()))
    subprocess.run(["git", "commit", "-m", f"auto-sync {stamp}"])
    return stamp


# -------------------
# STATUS
# -------------------
def status():
    events = load_events()
    graph = build_graph(events)

    print("=== IMA UNIFIED QGE+EVENT KERNEL ===")
    print("EVENTS:", len(events))
    print("NODES:", len(graph["nodes"]))
    print("EDGES:", len(graph["edges"]))


# -------------------
# CLI
# -------------------
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "ask":
        print(ask(" ".join(sys.argv[2:])))
        git_snapshot()
        return

    if cmd == "status":
        status()
        return

    if cmd == "sync":
        print(git_snapshot())
        return


if __name__ == "__main__":
    main()
