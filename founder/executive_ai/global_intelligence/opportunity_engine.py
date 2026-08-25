
from founder.executive_ai.global_intelligence.opportunity_ranker import rank_opportunity
from founder.executive_ai.global_intelligence.opportunity_memory import get_entities


def evaluate_world():

    entities = get_entities()
    results=[]

    for entity in entities:
        result = rank_opportunity(entity)

        result["reasoning"] = {
            "entity_type": entity.get("type"),
            "signals": result.get("signals",[]),
            "recommended_direction":
                "partnership"
                if entity.get("type")=="company"
                else "impact"
        }

        results.append(result)

    # Canonical decision score:
    # combines strategic opportunity with economic intelligence.
    results.sort(
        key=lambda x: x.get(
            "final_score",
            x.get("opportunity_score", 0)
        ),
        reverse=True
    )

    return {
        "total":len(results),
        "top_opportunities":results[:10],
        "all_opportunities":results
    }
