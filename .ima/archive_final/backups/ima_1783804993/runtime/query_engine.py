import json
import os
import sys
import time

from stream import emit

MEMORY = ".ima/memory_log.jsonl"
INDEX = ".ima/global_index.json"

# -------------------------
# LOAD MEMORY (legacy safe)
# -------------------------
def load_memory():
    if not os.path.exists(MEMORY):
        return []
    try:
        with open(MEMORY) as f:
            return [json.loads(l) for l in f if l.strip()]
    except:
        return []

# -------------------------
# SCORE ENGINE (stream-ready)
# -------------------------



def score(path, query):
    base = 1.0

    pth = path.lower().replace("\\", "/")
    qry = query.lower()

    if qry in pth:
        base += 50

    if "log" in pth:
        base += 10

    if "core" in pth:
        base += 5

    if "ima" in pth:
        base += 2

    if "orchestration" in pth or "squad" in pth:
        base += 15

    return base

