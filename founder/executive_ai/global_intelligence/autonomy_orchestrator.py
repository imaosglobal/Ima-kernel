"""IMA autonomous executive cycle: company control -> demand -> graph -> matching -> action queue."""
from __future__ import annotations
import json, time
from pathlib import Path
from .demand_capture import scan_all_sources, save as save_demand
from .global_opportunity_graph import build as build_graph
from .deal_hunter import match_leads, build_actions, status
from .company_os import run as run_company_os

ROOT = Path("founder/data")
STATE = ROOT / "ima_autonomy_state.json"
LOG = ROOT / "ima_autonomy_log.jsonl"

def write_state(state):
    ROOT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def log(event):
    ROOT.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def cycle():
    started = time.time()
    try:
        demand_rows, procurement_status = scan_all_sources()
        demand = save_demand(demand_rows)
        graph = build_graph()
        matches = match_leads()
        actions = build_actions(matches)
        company = run_company_os()
        result = {"ok": True, "demand_signals": len(demand), "graph": graph,
                  "matches": len(matches), "actions": len(actions), "status": status(),
                  "company_os": company, "procurement_sources": procurement_status, "execution_policy": "proof-gated",
                  "started_at": started, "finished_at": time.time()}
    except Exception as exc:
        result = {"ok": False, "error": repr(exc), "execution_policy": "proof-gated",
                  "started_at": started, "finished_at": time.time()}
    write_state(result); log({"event": "autonomy_cycle", **result}); return result

def main():
    print(json.dumps(cycle(), ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
