from http.server import BaseHTTPRequestHandler, HTTPServer
from html.parser import HTMLParser
import json, time, hashlib
from pathlib import Path

OUT = Path("learning/data/ori_facebook_ingested.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/browser":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0"))
        html = self.rfile.read(length).decode("utf-8", errors="ignore")

        parser = TextParser()
        parser.feed(html)

        text = " ".join(parser.parts)
        text = " ".join(text.split())

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"EMPTY")
            return

        h = hashlib.sha256(text.encode("utf-8")).hexdigest()

        record = {
            "creator_id": "creator_001",
            "creator": "Ori Cohen",
            "source": "Ori Cohen — Facebook Creator Source",
            "source_url": "https://www.facebook.com/share/1FFdWxZt2a/",
            "content": text,
            "content_hash": h,
            "content_type": "browser_page_text",
            "ingestion_method": "authenticated_browser_bridge",
            "read_only": True,
            "timestamp": time.time(),
            "provenance": {
                "source": "Facebook browser session",
                "canonical": True,
                "creator_id": "creator_001"
            }
        }

        with OUT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            json.dumps({
                "ok": True,
                "chars": len(text),
                "content_hash": h
            }, ensure_ascii=False).encode()
        )

    def log_message(self, *args):
        pass

print("IMA BROWSER HTML BRIDGE")
print("POST http://127.0.0.1:8770/browser")
HTTPServer(("127.0.0.1", 8770), Handler).serve_forever()
