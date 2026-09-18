"""IMA Company OS: executive control plane for product, engineering, QA, sales, finance and operations."""
from __future__ import annotations
import json, time
from pathlib import Path

ROOT = Path("founder/data")
STATE = ROOT / "ima_company_os.json"
ROLES = ("ceo","product","engineering","qa","design","marketing","sales","customer_success","recruiting","finance","legal_ops","security","growth")


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception as exc:
        return {"_error": repr(exc)}


def assess():
    autonomy = load(ROOT / "ima_autonomy_state.json")
    graph = load(ROOT / "global_opportunity_graph.json")
    routes = load(ROOT / "global_money_routes.json")
    pipeline = load(ROOT / "commerce_pipeline.json")
    deals = load(ROOT / "deal_hunter_opportunities.json")
    leads = load(ROOT / "approved_mailing_contacts.json")
    return {
        "timestamp": time.time(), "roles": list(ROLES),
        "engineering": {"autonomy_cycle_ok": autonomy.get("ok", False)},
        "qa": {"proof_gated": autonomy.get("execution_policy") == "proof-gated"},
        "commercial": {"opportunities": len(graph) if isinstance(graph, list) else 0,
                        "money_routes": len(routes) if isinstance(routes, list) else 0,
                        "deals": len(deals) if isinstance(deals, list) else 0},
        "finance": {"pipeline_records": len(pipeline) if isinstance(pipeline, list) else 0},
        "crm": {"approved_marketing_contacts": len(leads) if isinstance(leads, list) else 0},
    }


def priorities(state):
    p = []
    if not state["engineering"]["autonomy_cycle_ok"]: p.append(("P0","engineering","restore autonomous cycle"))
    if not state["qa"]["proof_gated"]: p.append(("P0","qa","restore proof gate before external actions"))
    if state["commercial"]["opportunities"] == 0: p.append(("P1","growth","increase real demand-source coverage"))
    if state["finance"]["pipeline_records"] == 0: p.append(("P1","finance","connect verified monetization routes"))
    if state["crm"]["approved_marketing_contacts"] == 0: p.append(("P1","sales","acquire explicit opt-in contacts through portal"))
    p += [("P2","product","improve end-to-end user journey"),
          ("P2","security","audit credentials and external action boundaries"),
          ("P2","design","keep product experience coherent and accessible")]
    return [{"priority":a,"owner":b,"task":c} for a,b,c in p]


def run():
    state = assess(); state["priorities"] = priorities(state)
    ROOT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return state

if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
