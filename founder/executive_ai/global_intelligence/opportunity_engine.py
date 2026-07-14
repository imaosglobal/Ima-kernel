from founder.executive_ai.global_intelligence.opportunity_ranker import rank_opportunity
from founder.executive_ai.global_intelligence.opportunity_memory import get_entities


def evaluate_world():

    entities=get_entities()

    results=[]

    for entity in entities:

        result=rank_opportunity(entity)

        result["reasoning"]=[]

        if entity.get("type")=="government":
            result["reasoning"].append(
                "יכולת השפעה רחבה"
            )

        if entity.get("type")=="company":
            result["reasoning"].append(
                "אפשרות לשיתוף פעולה עסקי"
            )

        if entity.get("type")=="nonprofit":
            result["reasoning"].append(
                "השפעה חברתית והתאמה למשימת IMA"
            )

        results.append(result)


    results.sort(
        key=lambda x:x["opportunity_score"],
        reverse=True
    )

    return {
        "total":len(results),
        "opportunities":results
    }
