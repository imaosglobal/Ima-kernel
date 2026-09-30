"""Create explicit learning gaps from knowledge, uncertainty and failures."""
from __future__ import annotations
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, Iterable

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/".ima"/"learning_gaps"
FILE=STATE/"gaps.jsonl"

def _id(value:str)->str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]

def detect(event:Dict[str,Any])->Dict[str,Any]:
    text=str(event.get("text") or event.get("topic") or "").strip()
    gaps=list(event.get("gaps",[]))
    if not gaps:
        gaps=["unknowns_to_research","prerequisites_to_identify","tools_to_discover","tests_to_define","ways_to_teach"]
    return {
        "schema":"IMA-LEARNING-GAP-1.0",
        "gap_id":_id(text+"|"+json.dumps(gaps,ensure_ascii=False,sort_keys=True)),
        "time":time.time(),
        "topic":text,
        "gaps":gaps,
        "evidence":event.get("evidence",[]),
        "status":"DISCOVERED",
        "next":["PRIORITIZED","RESEARCHING","TESTING","VERIFIED","TAUGHT"],
    }

def record(event:Dict[str,Any])->Dict[str,Any]:
    gap=detect(event)
    STATE.mkdir(parents=True,exist_ok=True)
    with FILE.open("a",encoding="utf-8") as fh:
        fh.write(json.dumps(gap,ensure_ascii=False,sort_keys=True)+"\n")
    return gap
