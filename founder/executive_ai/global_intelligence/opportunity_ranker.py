import time


def rank_opportunity(entity):
    score = 0
    reasons = []

    entity_text = str(entity).lower()

    if entity.get("type") in ["government","company","nonprofit"]:
        score += 20
        reasons.append("strategic entity")

    if "ai" in entity_text:
        score += 25
        reasons.append("AI alignment")

    if "need" in entity_text or "problem" in entity_text:
        score += 20
        reasons.append("clear demand signal")

    if "market" in entity_text or "customer" in entity_text:
        score += 15
        reasons.append("market relevance")

    if "funding" in entity_text or "startup" in entity_text:
        score += 10
        reasons.append("growth potential")

    return {
        "entity": entity,
        "opportunity_score": score,
        "signals": reasons,
        "timestamp": time.time()
    }
