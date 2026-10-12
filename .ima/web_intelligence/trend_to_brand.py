"""IMA Trend-to-Brand Engine.

Public-signal research only. It scores opportunities but never buys, publishes,
contacts creators, orders inventory, or claims commercial results.
"""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
STATE=ROOT/".ima/web_intelligence/trend_to_brand_state.json"

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
def digest(v): return hashlib.sha256(v.encode()).hexdigest()[:20]

def _score(item, independent_sources=1, persistence=0.0, purchase_intent=0.0,
           competition=0.5, safety=0.5, testability=0.5):
    viral=min(1.0,max(0.0,float(item.get("signal_strength",0.0))))
    return round(100*(0.22*viral+0.18*min(1,independent_sources/3)+
                      0.18*persistence+0.14*purchase_intent+
                      0.10*(1-competition)+0.08*safety+0.10*testability),2)

def build_card(item, independent_sources=1, persistence=0.0, purchase_intent=0.0,
               competition=0.5, safety=0.5, testability=0.5):
    score=_score(item,independent_sources,persistence,purchase_intent,competition,safety,testability)
    return {
      "id":digest(json.dumps(item,sort_keys=True)),
      "status":"RESEARCH_ONLY",
      "opportunity_score":score,
      "problem":item.get("problem"),
      "audience":item.get("audience"),
      "demand_evidence":[{"source":item.get("source"),"observed_at":item.get("observed_at")}],
      "independent_sources":independent_sources,
      "facts":item.get("facts",[]),
      "estimates":item.get("estimates",[]),
      "hypotheses":item.get("hypotheses",[]),
      "mvp":item.get("mvp"),
      "cost_range":item.get("cost_range"),
      "supplier_candidates":item.get("supplier_candidates",[]),
      "regulatory_notes":item.get("regulatory_notes",[]),
      "risks":item.get("risks",[]),
      "cheap_experiment":item.get("cheap_experiment"),
      "success_metrics":item.get("success_metrics",[]),
      "stop_conditions":item.get("stop_conditions",[]),
      "next_action":"collect independent public evidence and validate demand before any commerce action",
      "commercial_action_allowed":False,
      "created_at":now(),
    }

def run(discovery_items=None):
    items=discovery_items or []
    cards=[]
    for item in items[:100]:
        if not isinstance(item,dict) or not item.get("url"): continue
        cards.append(build_card(item))
    state={"schema":"IMA-TREND-TO-BRAND-1.0","timestamp":now(),
           "candidate_count":len(cards),"cards":cards,
           "policy":{"public_sources_only":True,"independent_evidence_required":True,
                     "no_private_data":True,"no_impersonation":True,
                     "no_spam":True,"no_purchase_or_publication":True,
                     "facts_estimates_hypotheses_separated":True}}
    STATE.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return state
