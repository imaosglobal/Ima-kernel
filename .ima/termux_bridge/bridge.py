#!/usr/bin/env python3
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOST = "127.0.0.1"
PORT = 8787

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            import subprocess, json as _json
            try:
                result = subprocess.run(
                    ["python", str(ROOT / "kernel/runtime/CANONICAL/python_bridge.py")],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                runtime = _json.loads(result.stdout)
                self.send_json({
                    "status": "ONLINE",
                    "bridge": "ima-termux",
                    "pid": os.getpid(),
                    "runtime": runtime
                })
            except Exception as e:
                self.send_json({
                    "status": "BRIDGE_ONLINE_RUNTIME_ERROR",
                    "error": str(e)
                }, 500)
        elif self.path == "/kernel":
            self.send_json({
                "root": str(ROOT),
                "exists": ROOT.exists()
            })
        else:
            self.send_json({"error": "not_found"}, 404)

    def do_POST(self):
        self.send_json({
            "error": "arbitrary_execution_disabled"
        }, 403)

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    print(f"IMA Termux bridge: http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
