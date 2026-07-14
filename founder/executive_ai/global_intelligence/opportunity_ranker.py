
def rank_opportunity(entity):

    score=0

    if entity.get("type") in [
        "government",
        "company",
        "nonprofit"
    ]:
        score+=30

    if "AI" in str(entity):
        score+=30

    if "need" in entity:
        score+=20

    return {
        "entity":entity,
        "opportunity_score":score
    }
