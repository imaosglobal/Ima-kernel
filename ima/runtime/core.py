import json, os, time

INDEX = ".ima/global_index.json"
MEMORY = ".ima/memory_log.jsonl"

def load_index():
    with open(INDEX) as f:
        return json.load(f)["files"]

def load_memory():
    if not os.path.exists(MEMORY):
        return []
    return [json.loads(l) for l in open(MEMORY) if l.strip()]



def ask(query):
    files = load_index()
    ranked = []

    for f in files:
        ranked.append((f["path"], base_score(f["path"], query)))

    ranked.sort(key=lambda x: x[1], reverse=True)

    for p, s in ranked[:10]:
        print(f"[{s:.2f}] {p}")

if __name__ == "__main__":
    import sys
    ask(" ".join(sys.argv[1:]))

def base_score(path, query):
    base = 1.0

    p = path.lower().replace('\\', '/')
    q = query.lower()

    if q in p:
        base += 50

    if 'log' in p:
        base += 10

    if 'core' in p:
        base += 5

    if 'ima' in p:
        base += 2

    if 'orchestration' in p or 'squad' in p:
        base += 15

    return base
