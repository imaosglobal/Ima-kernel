import json, time

LEDGER = ".ima/ledger.jsonl"


# -------------------------
# EVENT SYSTEM
# -------------------------
def emit(t, **data):
    e = {"ts": time.time(), "type": t, "data": data}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(e) + "\n")


def load_events():
    try:
        return [json.loads(l) for l in open(LEDGER) if l.strip()]
    except:
        return []


# -------------------------
# STATE GRAPH
# -------------------------
def build_graph(events):
    graph = {
        "nodes": {},
        "edges": []
    }

    for e in events:
        t = e["type"]
        d = e.get("data", {})

        if t == "QUESTION":
            qid = d.get("id")
            graph["nodes"][qid] = {
                "text": d.get("text"),
                "type": "question"
            }

        if t == "ANSWER":
            graph["edges"].append({
                "from": d.get("q"),
                "to": d.get("a"),
                "weight": 1
            })

        if t == "FACT":
            graph["nodes"][d.get("id")] = {
                "text": d.get("text"),
                "type": "fact"
            }

    return graph


# -------------------------
# QUESTION ENGINE
# -------------------------
def expand_question(q):
    return [
        q,
        q + " (context)",
        q + " (contradiction check)",
        q + " (external lookup needed?)"
    ]


# -------------------------
# ANSWER SPACE (SIMPLIFIED)
# -------------------------
def answer_space(q):
    return {
        "hypotheses": [
            {"answer": "A", "score": 0.5},
            {"answer": "B", "score": 0.3},
            {"answer": "UNKNOWN", "score": 0.2}
        ]
    }


# -------------------------
# EXTERNAL LAYER (PLACEHOLDERS)
# -------------------------
def web_search(q):
    return ["(external web disabled in local runtime)"]

def git_history():
    return ["(git history placeholder)"]


# -------------------------
# PIPELINE
# -------------------------
def ask(question):
    qid = str(int(time.time()))

    emit("QUESTION", id=qid, text=question)

    expanded = expand_question(question)
    answers = answer_space(question)

    return {
        "id": qid,
        "expanded": expanded,
        "answers": answers
    }


def status():
    events = load_events()
    graph = build_graph(events)



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        status()
    elif sys.argv[1] == "ask":
    else:
        status()
