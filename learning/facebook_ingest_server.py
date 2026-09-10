from __future__ import annotations

import hashlib
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

OUT = Path("learning/data/ori_facebook_ingested.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

SOURCE = "Ori Cohen — Facebook Creator Source"
SOURCE_URL = "https://www.facebook.com/share/1FFdWxZt2a/"
CREATOR_ID = "creator_001"


def normalize(text: str) -> str:
    return " ".join((text or "").split())


def content_hash(text: str) -> str:
    return hashlib.sha256(
        normalize(text).encode("utf-8")
    ).hexdigest()


def already_exists(h: str) -> bool:
    if not OUT.exists():
        return False

    with OUT.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                if json.loads(line).get("content_hash") == h:
                    return True
            except Exception:
                continue

    return False


class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/ingest":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        text = normalize(raw.decode("utf-8", errors="ignore"))

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"EMPTY")
            return

        h = content_hash(text)

        if already_exists(h):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"DUPLICATE")
            return

        record = {
            "creator_id": CREATOR_ID,
            "creator": "Ori Cohen",
            "source": SOURCE,
            "source_url": SOURCE_URL,
            "content": text,
            "content_hash": h,
            "content_type": "creator_content",
            "ingestion_method": "browser_bridge",
            "read_only": True,
            "timestamp": time.time(),
            "provenance": {
                "source": SOURCE,
                "canonical": True,
                "creator_id": CREATOR_ID,
            },
        }

        with OUT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"INGESTED")

    def log_message(self, format, *args):
        return


print("IMA FACEBOOK INGEST SERVER")
print("Listening: 127.0.0.1:8765")
print("Output:", OUT)

HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
