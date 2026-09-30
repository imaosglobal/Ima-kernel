"""Anonymous per-user memory isolated from founder/private IMA memory."""
import hashlib
import os
import sqlite3
import threading
import time
from pathlib import Path

_DB = Path(os.environ.get("PUBLIC_MEMORY_DB", ".ima/public_memory.sqlite3"))
_LOCK = threading.RLock()
_SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  created_at REAL NOT NULL,
  question TEXT NOT NULL,
  response TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_user_time
ON messages(user_id, created_at);
"""

def _safe_user_id(user_id):
    return hashlib.sha256(str(user_id or "anonymous").strip().encode()).hexdigest()

def _connect():
    _DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(_DB), timeout=10)
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(_SCHEMA)
    return con
def append(user_id, question, response):
    with _LOCK, _connect() as con:
        con.execute(
            "INSERT INTO messages(user_id, created_at, question, response) VALUES (?, ?, ?, ?)",
            (_safe_user_id(user_id), time.time(), question, response),
        )

def recent(user_id, limit=20):
    with _LOCK, _connect() as con:
        rows = con.execute(
            """SELECT created_at, question, response
               FROM messages WHERE user_id=?
               ORDER BY id DESC LIMIT ?""",
            (_safe_user_id(user_id), int(limit)),
        ).fetchall()
    return [{"time": r[0], "question": r[1], "response": r[2]} for r in reversed(rows)]

def recall(user_id, query, limit=5):
    q = (query or "").lower().strip()
    rows = recent(user_id, 100)
    if not q:
        return rows[-limit:]
    words = [w for w in q.split() if len(w) > 2]
    scored = []
    for item in rows:
        hay = (item["question"] + " " + item["response"]).lower()
        score = sum(1 for word in words if word in hay)
        if score:
            scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[:limit]]
