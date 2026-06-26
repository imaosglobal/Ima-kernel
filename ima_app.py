#!/usr/bin/env python3
import time
import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(BASE, ".ima_ledger.jsonl")
LOCK = os.path.join(BASE, ".ima_git.lock")


def load_events():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, "r") as f:
        return [json.loads(l) for l in f if l.strip()]


def emit(event_type, **data):
    e = {"ts": time.time(), "type": event_type, "data": data}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(e) + "\n")
    return e


def answer(q, memory):
    qn = q.strip().lower()

    recent = [e["data"].get("text") for e in memory if e["type"] == "QUESTION" and "text" in e["data"]][-20:]
    if qn in [r.lower() for r in recent]:
        return "כבר שאלת את זה."

    return f"אני איתך. הבנתי: {q}"


def ask(q):
    mem = load_events()
    emit("QUESTION", text=q)
    res = answer(q, mem)
    emit("ANSWER", text=res)
    return {"question": q, "answer": res}


def git_snapshot():
    if os.path.exists(LOCK):
        return
    open(LOCK, "w").close()
    try:
        subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
            subprocess.run(["git", "commit", "-m", f"auto {int(time.time())}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        os.remove(LOCK)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        res = ask(body.get("text", ""))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())


def daemon():
    print("[IMA] daemon started")
    last = 0
    while True:
        try:
            ev = load_events()
            if len(ev) != last:
                last = len(ev)
                print("[IMA] events:", last)

                for e in ev[-10:]:
                    if e["type"] == "QUESTION":
                        ans = answer(e["data"]["text"], ev)
                        emit("ANSWER", text=ans)

                git_snapshot()

            time.sleep(1)
        except KeyboardInterrupt:
            break


def server():
    print("[IMA] API on :8000")
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()


def main():
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "ask":
        print(ask(" ".join(sys.argv[2:])))
    elif cmd == "daemon":
        daemon()
    elif cmd == "server":
        server()
    else:
        print("usage: ask | daemon | server")


if __name__ == "__main__":
    main()
