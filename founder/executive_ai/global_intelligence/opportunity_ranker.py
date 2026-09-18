import time

from founder.executive_ai.action_engine.feedback_engine import analyze_feedback


def rank_opportunity(entity):
    score = 0
    reasons = []
    entity_text = str(entity).lower()
    entity_type = entity.get("type")

    if entity_type == "commercial_deal":
        score += 35
        reasons.append("commercial opportunity")
        payout = entity.get("payout_amount")
        if isinstance(payout, (int, float)) and payout > 0:
            score += min(40, int(payout / 10))
            reasons.append("explicit payout")
        if entity.get("geography") == "global":
            score += 10
            reasons.append("global buyer demand")
        if entity.get("consent_required"):
            reasons.append("consent gate active")
        if entity.get("verification_status", "").startswith("public-listing"):
            score += 10
            reasons.append("public listing verified")
        return {
            "entity": entity,
            "opportunity_score": min(score, 100),
            "signals": reasons,
            "timestamp": time.time(),
        }

    if not entity_type:
        category = str(entity.get("category", "")).lower()
        if category == "government" or entity.get("source") == "government":
            entity_type = "government"
        elif category in ["ai", "company", "startup"]:
            entity_type = "company"
        elif category in ["nonprofit", "ngo", "foundation"]:
            entity_type = "nonprofit"

    if entity_type in ["government", "company", "nonprofit"]:
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

    feedback = analyze_feedback()
    lessons = " ".join(feedback.get("lessons", [])).lower()
    if entity_type == "government" and "public impact" in lessons:
        score += 5
        reasons.append("learned government impact strategy")
    if "startup" in entity_text or entity_type == "company":
        if "positive outreach" in lessons:
            score += 10
            reasons.append("previous positive signal")

    entity_name = entity.get("name", "").lower()
    for record in feedback.get("records", []):
        target = str(record.get("target", "")).lower()
        if target and target in entity_name:
            if record.get("status") in ["no_response", "failed"]:
                score -= 5
                reasons.append("entity negative historical signal")
            if record.get("status") in ["response_received", "positive_response", "success"]:
                score += 5
                reasons.append("entity confirmed positive signal")

    return {
        "entity": entity,
        "opportunity_score": max(0, score),
        "signals": list(dict.fromkeys(reasons)),
        "timestamp": time.time(),
    }
