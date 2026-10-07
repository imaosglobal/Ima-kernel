#!/usr/bin/env python3
"""IMA adaptation evaluator.

Turns discovered knowledge into bounded, reviewable improvement candidates.
It never edits product code directly: candidates must pass evidence and tests.
"""
from __future__ import annotations
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
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
    seen=discovery.get("seen",{}) if isinstance(discovery.get("seen",{}),dict) else {}
    recent_items=discovery.get("recent_items",[])
    if not isinstance(recent_items,list):
        recent_items=[]
    discovery_item_count=len(seen)
    candidates=[]
    for item in recent_items[:50]:
        if not isinstance(item,dict) or not item.get("url"):
            continue
        source_text=f"{item.get('title','')} {item.get('source','')}".lower()
        dimension=next((dim for dim in dimensions if dim.lower() in source_text), None)
        candidates.append({
            "id":digest(item.get("id",item["url"])),
            "dimension":dimension,
            "status":"CANDIDATE",
            "candidate_kind":"source_review",
            "title":item.get("title",""),
            "source_url":item["url"],
            "source":item.get("source",""),
            "kind":item.get("kind",""),
            "observed_at":item.get("observed_at"),
            "evidence_required":matrix.get("acceptance",[]),
            "source_state_timestamp":discovery.get("last_run"),
            "decision":"compare_specific_source_evidence_against_current_implementation",
            "adoption_blocked":True,
            "evidence_status":"source_metadata_available_change_detail_required",
            "source_state_path":".ima/web_intelligence/state.json",
            "discovery_item_count":discovery_item_count
        })
    if not candidates:
        for dim in dimensions:
            candidates.append({
                "id":digest(dim),
                "dimension":dim,
                "status":"REVIEW_ONLY",
                "candidate_kind":"dimension_review",
                "evidence_required":matrix.get("acceptance",[]),
                "source_state_timestamp":discovery.get("last_run"),
                "decision":"await_specific_discovery_item",
                "adoption_blocked":True,
                "evidence_status":"no_recent_discovery_items",
                "source_state_path":".ima/web_intelligence/state.json",
                "discovery_item_count":discovery_item_count
            })

    state={
        "schema":"IMA-ADAPTATION-STATE-1.0",
        "timestamp":now(),
        "dimensions":dimensions,
        "candidate_count":len(candidates),
        "candidate_kind":"source_review" if recent_items else "dimension_review",
        "discovery_item_count":discovery_item_count,
        "discovery_last_run":discovery.get("last_run"),
        "rule":"observe -> compare -> prototype -> test -> verify -> adopt/reject -> record",
        "adoption_gate":"blocked_until_candidate_has_specific_source_evidence_and_test"
    }
    STATE.parent.mkdir(parents=True,exist_ok=True)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    OUT.write_text(json.dumps({"schema":"IMA-ADAPTATION-CANDIDATES-1.0","timestamp":state["timestamp"],"candidates":candidates},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(state,ensure_ascii=False,indent=2))

if __name__=="__main__":
    run()
