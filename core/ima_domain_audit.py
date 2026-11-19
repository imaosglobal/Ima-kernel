"""Read-only canonical domain audit; never creates a second system of record."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/".ima"/"CANONICAL_DOMAIN_AUDIT.json"

def load():
    try:
        data=json.loads(PATH.read_text(encoding="utf-8"))
        return data if isinstance(data,dict) else {}
    except Exception:
        return {}

def snapshot():
    data=load()
    domains=data.get("domains",[])
    counts={}
    for d in domains:
        counts[d.get("state","UNKNOWN")]=counts.get(d.get("state","UNKNOWN"),0)+1
    return {"id":data.get("id"),"version":data.get("version"),"domain_count":len(domains),"evidence_counts":counts,"priority_order":data.get("priority_order",[])}
