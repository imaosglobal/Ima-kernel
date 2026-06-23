import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / ".ima" / "global_index.json"

TYPE_SCORE = {
    "core": 10,
    "runtime": 8,
    "system": 6,
    "script": 5,
    "data": 3,
    "log": 2,
    "other": 1
}

def ask(query):
    with open(INDEX) as f:
        data = json.load(f)

    q = query.lower()
    results = []

    for f in data.get("files", []):
        path = f["path"]
        t = f.get("type", "other")

        if q in path.lower():
            score = TYPE_SCORE.get(t, 1)

            results.append((score, t, path))

    results.sort(reverse=True)

    if not results:
        return "No relevant memory found."

    return "\n".join([f"[{t}] {p}" for _, t, p in results[:10]])

if __name__ == "__main__":
    cmd = sys.argv[1]

    if cmd == "ask":
        print(ask(" ".join(sys.argv[2:])))
