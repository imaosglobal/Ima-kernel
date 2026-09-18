"""Generic commerce pipeline for IMA Deal Hunter.
Keeps discovery, eligibility, authorization, submission, conversion and payout distinct.
"""
from __future__ import annotations
import hashlib,json,time
from pathlib import Path
from .marketplace_adapters import all_marketplaces,route_for
ROOT=Path("founder/data")
STATE=ROOT/"commerce_pipeline.json"
STAGES=("DISCOVERED","VERIFIED","ELIGIBLE","READY","AUTHORIZED","SUBMITTED","CONVERTED","PAID")

def _load():
    try:return json.loads(STATE.read_text(encoding="utf-8"))
    except:return []
def _save(rows):
    STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
def create(deal,marketplace):
    routes=route_for(deal); route=next((x for x in routes if x["name"]==marketplace),None)
    if not route:return None
    key=str(deal.get("id"))+marketplace
    row={"pipeline_id":hashlib.sha256(key.encode()).hexdigest()[:20],"deal_id":deal.get("id"),"marketplace":marketplace,"stage":"DISCOVERED","route":route,"created_at":time.time(),"updated_at":time.time()}
    rows=[r for r in _load() if r.get("pipeline_id")!=row["pipeline_id"]]; rows.append(row); _save(rows); return row

def advance(pipeline_id,stage,proof=None):
    if stage not in STAGES:raise ValueError("invalid stage")
    rows=_load()
    for r in rows:
        if r.get("pipeline_id")==pipeline_id:
            current=STAGES.index(r["stage"]); target=STAGES.index(stage)
            if target<current:raise ValueError("cannot move pipeline backward")
            if target>current+1:raise ValueError("stages must advance one step at a time")
            if stage in ("AUTHORIZED","SUBMITTED") and not proof:raise ValueError("authorization/submission proof required")
            r["stage"]=stage;r["updated_at"]=time.time()
            if proof:r.setdefault("proof",[]).append(proof)
            _save(rows);return r
    raise KeyError("pipeline not found")

def summary():
    rows=_load();return {s:sum(r.get("stage")==s for r in rows) for s in STAGES}|{"pipelines":len(rows),"marketplaces":len(all_marketplaces())}

if __name__=="__main__":
    print(json.dumps(summary(),ensure_ascii=False,indent=2))
