import json
import subprocess
#!/usr/bin/env python3
import time, json, os, subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(BASE, ".ima_ledger.jsonl")
LOCK = os.path.join(BASE, ".ima_git.lock")

# -------------------------
# STORAGE
# -------------------------
def load_events():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, "r") as f:
        return [json.loads(l) for l in f if l.strip()]

def emit(event_type, **data):
    e = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }
    with open(LEDGER, "a") as f:
        f.write(json.dumps(e) + "\n")
    return e

# -------------------------
# BRAIN (SINGLE)
# -------------------------
def answer(q, memory):
    qn = q.strip().lower()

    recent_q = [
        e["data"].get("text")
        for e in memory
        if e["type"] == "QUESTION"
    ][-20:]

    if qn in [r.lower() for r in recent_q if r]:
        return "כבר שאלת את זה."

    return f"אני כאן איתך. הבנתי: {q}"

# -------------------------
# ASK PIPELINE
# -------------------------
def ask(q):
    mem = load_events()
    emit("QUESTION", text=q)
    res = answer(q, mem)
    emit("ANSWER", text=res)
    return {"question": q, "answer": res}

# -------------------------
# SAFE GIT SNAPSHOT
# -------------------------
def git_snapshot():
    if os.path.exists(LOCK):
        return

    open(LOCK, "w").close()

    try:
        subprocess.run(["git", "add", "-A"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
            subprocess.run(["git", "commit", "-m", f"auto {int(time.time())}"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    finally:
        os.remove(LOCK)

# -------------------------
# DAEMON (FIXED - NO FLOOD)
# -------------------------
def daemon():

    processed = set()

    while True:
        try:
            events = load_events()

            for e in events:
                eid = str(e["ts"])

                if eid in processed:
                    continue

                processed.add(eid)

                # רק שאלות
                if e["type"] != "QUESTION":
                    continue

                q = e["data"]["text"]
                res = answer(q, events)

                emit("ANSWER", text=res)

            git_snapshot()
            time.sleep(1)

        except KeyboardInterrupt:
            break

# -------------------------
# API
# -------------------------
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        res = ask(body.get("text", ""))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())

def server():
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()

# -------------------------
# CLI
# -------------------------
def main():
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "ask":
    elif cmd == "daemon":
        daemon()
    elif cmd == "server":
        server()
    else:

if __name__ == "__main__":
    main()
