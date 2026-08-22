#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time

# -------------------------
# MEMORY STORE (multi-user)
# -------------------------
USERS = {}

def get_user(uid):
    if uid not in USERS:
        USERS[uid] = {
            "history": [],
            "topic": None,
            "last": None
        }
    return USERS[uid]

# -------------------------
# CORE BRAIN (simple but stable)
# -------------------------
def brain(user, text):
    u = get_user(user)

    t = text.lower().strip()
    u["history"].append(t)

    # detect topic
    if "תודעה" in t:
        u["topic"] = "consciousness"
        reply = "תודעה היא חוויה של מודעות לעצמך ולעולם."
    elif "קשה" in t:
        u["topic"] = "emotion"
        reply = "אני כאן איתך. מה אתה מרגיש עכשיו?"
    elif "מי אני" in t:
        u["topic"] = "identity"
        reply = "זו שאלה עמוקה. מה הביא אותך לשאול את זה?"
    elif t in ["היי", "hello", "hi"]:
        u["topic"] = "greeting"
        reply = "אני כאן איתך. איך אתה מרגיש באמת?"
    else:
        u["topic"] = "general"
        reply = "אני איתך. תמשיך."

    u["last"] = reply
    return reply

# -------------------------
# HTTP API
# -------------------------
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        uid = body.get("user", "anon")
        text = body.get("text", "")

        response = brain(uid, text)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({
            "reply": response,
            "ts": time.time()
        }).encode())

# -------------------------
# SERVER
# -------------------------
def run():
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    server.serve_forever()

if __name__ == "__main__":
    run()
