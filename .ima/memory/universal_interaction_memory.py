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

SCHEMA = "IMA-UNIVERSAL-INTERACTION-MEMORY-1.0"
STATUSES = {"PLANNED","ATTEMPTED","EXECUTED","VERIFIED","FAILED","GAPS_RECORDED"}

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
        CREATE INDEX IF NOT EXISTS idx_interaction_user_time
          ON interaction_memory(user_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_interaction_learning
          ON interaction_memory(authorized_learning);
        """)

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
