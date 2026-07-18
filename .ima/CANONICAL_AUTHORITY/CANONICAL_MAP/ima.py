import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INDEX_PATH = ROOT / ".ima" / "global_index.json"
GRAPH_PATH = ROOT / ".ima" / "graph.json"
MEM_PATH = ROOT / ".ima" / "memory_log.jsonl"


# ----------------------------
# LOADERS
# ----------------------------
def load_index():
    with open(INDEX_PATH) as f:
        return json.load(f)


def load_graph():
    with open(GRAPH_PATH) as f:
        return json.load(f)


# ----------------------------
# SEED
# ----------------------------
def seed(files, query):
    q = query.lower()
    return {
        f["path"]: 1.0
        for f in files
        if q in f["path"].lower()
    }


# ----------------------------
# GRAPH EXPANSION
# ----------------------------
def expand(graph, scores):
    for e in graph.get("edges", []):
        w = e.get("weight", 0.5)

        if e["from"] in scores:
            scores[e["to"]] = scores.get(e["to"], 0) + scores[e["from"]] * w

        if e["to"] in scores:
            scores[e["from"]] = scores.get(e["from"], 0) + scores[e["to"]] * w

    return scores


# ----------------------------
# MEMORY REINFORCEMENT
# ----------------------------
def reinforce(query, scores):
    try:
        with open(MEM_PATH) as f:
            for line in f:
                ev = json.loads(line)

                if ev.get("query") == query:
                    for path, score in ev.get("top", []):
                        scores[path] = scores.get(path, 0) + score * 0.1
    except:
        pass

    return scores


# ----------------------------
# LOGGING
# ----------------------------
def log(query, ranked):
    event = {
        "ts": time.time(),
        "query": query,
        "top": ranked[:5]
    }

    with open(MEM_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")


# ----------------------------
# ASK ENGINE
# ----------------------------
def ask(query):
    index = load_index()
    graph = load_graph()

    files = index.get("files", [])

    scores = seed(files, query)
    scores = expand(graph, scores)
    scores = reinforce(query, scores)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if not ranked:
        print("No relevant memory found.")
        return

    log(query, ranked)

    for path, score in ranked[:15]:
        tag = "file"
        if "log" in path.lower():
            tag = "log"
        elif "core" in path.lower():
            tag = "core"

        print(f"[{tag} | {score:.2f}] {path}")


# ----------------------------
# REBUILD PLACEHOLDER
# ----------------------------
def rebuild():
    print("Use: python3 .ima/rebuild_index.py && python3 .ima/build_graph.py")


# ----------------------------
# CLI
# ----------------------------
def main():
    if len(sys.argv) < 2:
        print("ima commands: ask | rebuild")
        return

    cmd = sys.argv[1]

    if cmd == "ask":
        ask(" ".join(sys.argv[2:]))

    elif cmd == "rebuild":
        rebuild()

    else:
        print("unknown command")


if __name__ == "__main__":
    main()
