from founder.executive_ai.global_intelligence.opportunity_ranker import rank_opportunity
from founder.executive_ai.global_intelligence.opportunity_memory import get_entities
from founder.executive_ai.global_intelligence.deal_hunter import load_saved


def evaluate_world():
    entities = get_entities()
    deal_entities = load_saved()
    combined = entities + [
        {
            **deal,
            "type": "commercial_deal",
            "name": deal.get("title", "Deal opportunity"),
            "category": deal.get("category", "general"),
        }
        for deal in deal_entities
        if deal.get("verification_status")
    ]

    results = []
    for entity in combined:
        result = rank_opportunity(entity)
        result["reasoning"] = {
            "entity_type": entity.get("type"),
            "signals": result.get("signals", []),
            "recommended_direction": "monetize"
            if entity.get("type") == "commercial_deal"
            else ("partnership" if entity.get("type") == "company" else "impact"),
        }
        results.append(result)

    results.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return {
        "total": len(results),
        "top_opportunities": results[:10],
        "all_opportunities": results,
    }
