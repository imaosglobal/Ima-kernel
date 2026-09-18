from __future__ import annotations
import hashlib, json, time
from pathlib import Path
from .global_source_registry import all_sources

ROOT = Path("founder/data")
SIGNALS = ROOT / "public_demand_signals.json"
GRAPH = ROOT / "global_opportunity_graph.json"
ROUTES = ROOT / "global_money_routes.json"

MONEY_MODELS = {
    "affiliate": "tracked_sale_or_lead",
    "referral": "qualified_introduction",
    "lead_fee": "qualified_lead",
    "reseller": "margin_or_revenue_share",
    "brokerage": "transaction_fee",
    "revshare": "recurring_revenue_share",
    "cpa": "conversion_action",
    "cpl": "qualified_lead",
    "cps": "sale",
    "deal_registration": "registered_business_deal",
}

def load(path):
    try: return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except Exception: return []

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def score(signal):
    score = 0
    if signal.get("public_demand"): score += 30
    if signal.get("category") not in (None, "general"): score += 20
    if signal.get("url"): score += 10
    if signal.get("contactability") == "known": score += 15
    if signal.get("opt_in_lead"): score += 25
    return min(100, score)

def routes_for(signal):
    category = signal.get("category", "general")
    routes = []
    for source in all_sources():
        if category in source["verticals"] or "all" in source["verticals"]:
            for model in source["monetization"]:
                routes.append({"source": source["name"], "model": model, "meaning": MONEY_MODELS.get(model, model), "url": source["url"], "access": source["access"]})
    return routes

def build():
    signals = load(SIGNALS)
    graph = []
    route_index = []
    for s in signals:
        routes = routes_for(s)
        node_id = hashlib.sha256((s.get("id", "") + "|global").encode()).hexdigest()[:20]
        graph.append({"node_id": node_id, "signal_id": s.get("id"), "category": s.get("category"), "title": s.get("title"), "url": s.get("url"), "score": score(s), "stage": "DISCOVERED", "routes": routes, "consent_required": True, "external_submission_proof": False, "created_at": time.time()})
        for route in routes:
            route_index.append({"node_id": node_id, **route})
    save(GRAPH, graph); save(ROUTES, route_index)
    return {"signals": len(signals), "opportunities": len(graph), "money_routes": len(route_index), "categories": sorted({x.get("category") for x in graph}), "graph_file": str(GRAPH), "routes_file": str(ROUTES)}

def summary():
    graph = load(GRAPH); routes = load(ROUTES)
    by_category = {}
    by_model = {}
    for x in graph: by_category[x.get("category", "general")] = by_category.get(x.get("category", "general"), 0) + 1
    for x in routes: by_model[x.get("model", "unknown")] = by_model.get(x.get("model", "unknown"), 0) + 1
    return {"opportunities": len(graph), "money_routes": len(routes), "by_category": by_category, "by_model": by_model}
