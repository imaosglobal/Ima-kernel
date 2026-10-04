#!/usr/bin/env python3
"""IMA adaptation evaluator.

Turns discovered knowledge into bounded, reviewable improvement candidates.
It never edits product code directly: candidates must pass evidence and tests.
"""
from __future__ import annotations
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"integrations/IMA_ADAPTATION_MATRIX.json"
STATE=ROOT/".ima/web_intelligence/adaptation_state.json"
OUT=ROOT/"artifacts/web-intelligence/adaptation_candidates.json"

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]

def load_json(path, default):
    if not path.exists(): return default
    return json.loads(path.read_text(encoding="utf-8"))

def run():
    matrix=load_json(MATRIX,{})
    discovery=load_json(ROOT/".ima/web_intelligence/state.json",{"seen":{},"last_run":None})
    dimensions=[x[0] for x in matrix.get("dimensions",[])]
    candidates=[]
    for dim in dimensions:
        key=digest(dim)
        candidates.append({
            "id":key,
            "dimension":dim,
            "status":"CANDIDATE",
            "evidence_required":matrix.get("acceptance",[]),
            "source_state_timestamp":discovery.get("last_run"),
            "decision":"evaluate_against_current_implementation_before_adoption"
        })
    state={
        "schema":"IMA-ADAPTATION-STATE-1.0",
        "timestamp":now(),
        "dimensions":dimensions,
        "candidate_count":len(candidates),
        "discovery_last_run":discovery.get("last_run"),
        "rule":"observe -> compare -> prototype -> test -> verify -> adopt/reject -> record"
    }
    STATE.parent.mkdir(parents=True,exist_ok=True)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    OUT.write_text(json.dumps({"schema":"IMA-ADAPTATION-CANDIDATES-1.0","timestamp":state["timestamp"],"candidates":candidates},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(state,ensure_ascii=False,indent=2))

if __name__=="__main__":
    run()
