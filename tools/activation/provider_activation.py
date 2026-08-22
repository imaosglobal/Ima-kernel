#!/data/data/com.termux/files/usr/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import subprocess
import json, time, webbrowser, threading

BASE = Path.home() / "ima_kernel"
STATE = BASE / ".ima/PUBLIC_PRODUCT/DEPLOYMENT/PROVIDER_ACTIVATION_STATE.json"
STATE.parent.mkdir(parents=True, exist_ok=True)

PORT = 8787

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/complete"):
            provider = self.path.split("provider=")[-1] if "provider=" in self.path else "unknown"

            data = {
                "provider": provider,
                "status": "COMPLETED",
                "updated": time.time()
            }

            STATE.write_text(json.dumps(data, indent=2))

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"IMA PROVIDER ACTIVATION COMPLETE")

        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"IMA ACTIVATION LISTENER")

def open_browser(provider):
    if provider == "supabase":
        url="https://supabase.com/dashboard"
    elif provider == "render":
        url="https://dashboard.render.com"
    else:
        url="https://google.com"

    subprocess.run(["termux-open-url", url])

if __name__ == "__main__":
    import sys

    provider = sys.argv[1] if len(sys.argv)>1 else "supabase"


    threading.Timer(2, open_browser, args=(provider,)).start()

    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
