
import time

from founder.executive_ai.action_engine.feedback_engine import analyze_feedback


def rank_opportunity(entity):

    score = 0
    reasons = []

    entity_text = str(entity).lower()

    # בסיס
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


    # למידה ממשוב עבר
    feedback = analyze_feedback()

    lessons = " ".join(
        feedback.get("lessons", [])
    ).lower()


    if entity.get("type") == "government":
        if "public impact" in lessons:
            score += 5
            reasons.append("learned government impact strategy")


    if "startup" in entity_text or entity.get("type")=="company":
        if "positive outreach" in lessons:
            score += 10
            reasons.append("previous positive signal")


    if "failed" in lessons or "no_response" in lessons:
        score -= 5
        reasons.append("negative historical signal")


    return {
        "entity": entity,
        "opportunity_score": score,
        "signals": reasons,
        "timestamp": time.time()
    }
