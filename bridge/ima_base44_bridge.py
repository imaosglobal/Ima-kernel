from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time
from pathlib import Path

ROOT = Path.home() / "Ima-kernel"
PORT = 8766

class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health":
            self.send_json({
                "ok": True,
                "service": "IMA Local Bridge",
                "root": str(ROOT),
                "timestamp": time.time()
            })
            return

        if self.path == "/manifest":
            self.send_json({
                "ok": True,
                "name": "IMA Local Bridge",
                "root": str(ROOT),
                "capabilities": [
                    "project_read",
                    "knowledge_read",
                    "memory_read",
                    "facebook_archive_read",
                    "android_bridge"
                ]
            })
            return

        self.send_json({"ok": False, "error": "not_found"}, 404)

    def do_POST(self):
        if self.path != "/sync":
            self.send_json({"ok": False, "error": "not_found"}, 404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body.decode())
        except Exception:
            self.send_json({"ok": False, "error": "invalid_json"}, 400)
            return

        self.send_json({
            "ok": True,
            "received": True,
            "timestamp": time.time(),
            "keys": list(payload.keys())
        })

    def log_message(self, *args):
        pass

print(f"IMA Local Bridge listening on 127.0.0.1:{PORT}")
HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
