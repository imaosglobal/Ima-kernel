"""Canonical Universal Conversation & Interaction Memory runtime.

Privacy-first extension of the existing per-user memory store. It never shares
private records into generalized learning unless explicitly authorized.
"""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from datetime import datetime, timezone

from public_memory import _connect, _LOCK, _safe_user_id

SCHEMA = "IMA-UNIVERSAL-INTERACTION-MEMORY-1.1"
STATUSES = {"PLANNED","ATTEMPTED","EXECUTED","VERIFIED","FAILED","GAPS_RECORDED"}
_SENSITIVE_MARKERS = ("BEGIN PRIVATE KEY", "bearer ", "authorization:", "api_key=", "apikey=", "password=", "passwd=", "secret=")

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def ensure_schema() -> None:
    with _LOCK, _connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS interaction_memory (
          id TEXT PRIMARY KEY,
          user_id TEXT NOT NULL,
          created_at TEXT NOT NULL,
          source TEXT NOT NULL,
          language TEXT,
          interface TEXT,
          participants TEXT,
          consent_status TEXT NOT NULL,
          original_content TEXT NOT NULL,
          translation_refs TEXT,
          actions TEXT,
          outcome TEXT,
          verification TEXT,
          uncertainty TEXT,
          temporal_class TEXT NOT NULL,
          evidence_refs TEXT,
          authorized_learning INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS memory_consent (
          user_id TEXT PRIMARY KEY,
          status TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          source TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memory_audit (
          id TEXT PRIMARY KEY,
          user_id TEXT NOT NULL,
          timestamp TEXT NOT NULL,
          action TEXT NOT NULL,
          record_id TEXT,
          result TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_interaction_user_time
          ON interaction_memory(user_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_interaction_learning
          ON interaction_memory(authorized_learning);
        """)

def set_consent(user_id: str, status: str, source: str="user") -> dict:
    if status not in {"GRANTED","DENIED","UNKNOWN"}:
        raise ValueError("invalid consent status")
    ensure_schema()
    ts=utc_now()
    uid=_safe_user_id(user_id)
    with _LOCK, _connect() as con:
        con.execute("INSERT INTO memory_consent(user_id,status,updated_at,source) VALUES(?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET status=excluded.status,updated_at=excluded.updated_at,source=excluded.source",(uid,status,ts,source))
        con.execute("INSERT INTO memory_audit(id,user_id,timestamp,action,record_id,result) VALUES(?,?,?,?,?,?)",(str(uuid.uuid4()),uid,ts,"CONSENT_UPDATE",None,status))
    return {"user_id":uid,"status":status,"updated_at":ts,"source":source}

def get_consent(user_id: str) -> dict:
    ensure_schema()
    uid=_safe_user_id(user_id)
    with _LOCK, _connect() as con:
        row=con.execute("SELECT status,updated_at,source FROM memory_consent WHERE user_id=?",(uid,)).fetchone()
    if not row:
        return {"status":"UNKNOWN","updated_at":None,"source":None}
    return {"status":row[0],"updated_at":row[1],"source":row[2]}

def audit_events(user_id: str, limit: int=100) -> list[dict]:
    ensure_schema()
    uid=_safe_user_id(user_id)
    with _LOCK, _connect() as con:
        rows=con.execute("SELECT timestamp,action,record_id,result FROM memory_audit WHERE user_id=? ORDER BY timestamp ASC LIMIT ?",(uid,int(limit))).fetchall()
    return [{"timestamp":r[0],"action":r[1],"record_id":r[2],"result":r[3]} for r in rows]

def _contains_secret(content: str) -> bool:
    lower=content.lower()
    return any(marker.lower() in lower for marker in _SENSITIVE_MARKERS)

def capture(*, user_id: str, source: str, content: str, consent: str,
            language: str|None=None, interface: str|None=None,
            participants: list[str]|None=None, translation_refs: list[str]|None=None,
            actions: list[dict]|None=None, outcome: str|None=None,
            verification: str|None=None, uncertainty: str|None=None,
            temporal_class: str="PRESENT", evidence_refs: list[str]|None=None,
            authorized_learning: bool=False, status: str="EXECUTED") -> dict:
    ensure_schema()
    if not content or not source:
        raise ValueError("source and content are required")
    if _contains_secret(content):
        raise ValueError("sensitive credential-like content is not eligible for memory storage")
    if consent not in {"GRANTED","DENIED","UNKNOWN"}:
        raise ValueError("invalid consent status")
    if temporal_class not in {"PAST","PRESENT","FUTURE"}:
        raise ValueError("invalid temporal class")
    if status not in STATUSES:
        raise ValueError("invalid status")
    if authorized_learning and consent != "GRANTED":
        raise ValueError("generalized learning requires explicit consent")
    event_id = str(uuid.uuid4())
    record = {
        "schema": SCHEMA, "id": event_id, "timestamp": utc_now(),
        "source": source, "language": language, "interface": interface,
        "participants": participants or [], "consent": consent,
        "content_hash": _digest(content), "status": status,
        "temporal_class": temporal_class,
    }
    with _LOCK, _connect() as con:
        con.execute(
          """INSERT INTO interaction_memory
          (id,user_id,created_at,source,language,interface,participants,consent_status,
           original_content,translation_refs,actions,outcome,verification,uncertainty,
           temporal_class,evidence_refs,authorized_learning)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
          (event_id, _safe_user_id(user_id), record["timestamp"], source, language,
           interface, json.dumps(participants or [],ensure_ascii=False),
           consent, content, json.dumps(translation_refs or [],ensure_ascii=False),
           json.dumps(actions or [],ensure_ascii=False), outcome, verification, uncertainty,
           temporal_class, json.dumps(evidence_refs or [],ensure_ascii=False),
           int(bool(authorized_learning))),
        )
    return record

def export_user_memory(user_id: str) -> list[dict]:
    ensure_schema()
    with _LOCK, _connect() as con:
        rows = con.execute(
          """SELECT id,created_at,source,language,interface,participants,consent_status,
                    original_content,translation_refs,actions,outcome,verification,uncertainty,
                    temporal_class,evidence_refs,authorized_learning
             FROM interaction_memory WHERE user_id=? ORDER BY created_at ASC""",
          (_safe_user_id(user_id),)).fetchall()
    keys=["id","timestamp","source","language","interface","participants","consent",
          "content","translation_refs","actions","outcome","verification","uncertainty",
          "temporal_class","evidence_refs","authorized_learning"]
    result=[]
    for row in rows:
        vals=list(row)
        for i in (5,8,9,14): vals[i]=json.loads(vals[i] or "[]")
        result.append(dict(zip(keys,vals)))
    return result

def delete_user_memory(user_id: str) -> int:
    ensure_schema()
    with _LOCK, _connect() as con:
        cur=con.execute("DELETE FROM interaction_memory WHERE user_id=?",( _safe_user_id(user_id),))
        return cur.rowcount

def learning_records() -> list[dict]:
    ensure_schema()
    with _LOCK, _connect() as con:
        rows=con.execute(
          "SELECT id,created_at,source,content_hash,verification,evidence_refs FROM interaction_memory WHERE authorized_learning=1 ORDER BY created_at ASC"
        ).fetchall()
    return [{"id":r[0],"timestamp":r[1],"source":r[2],"content_hash":r[3],
             "verification":r[4],"evidence_refs":json.loads(r[5] or "[]")} for r in rows]
