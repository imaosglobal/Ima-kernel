import os, json, time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080
STATE = {"last": None}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()

        STATE["last"] = body

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({
            "ok": True,
            "received": body,
            "ts": time.time()
        }).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(STATE).encode())

HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
