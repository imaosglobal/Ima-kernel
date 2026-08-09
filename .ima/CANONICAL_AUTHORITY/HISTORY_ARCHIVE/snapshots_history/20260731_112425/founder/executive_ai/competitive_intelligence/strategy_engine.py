import time

from founder.executive_ai.competitive_intelligence.competitor_analyzer import analyze_market
from founder.executive_ai.customer_intelligence.market_learning import learn_patterns
from founder.executive_ai.operating_system.context import get_context
from founder.executive_ai.operating_system.outcome_memory import get_outcomes


def generate_strategy(question=""):

    context = get_context()
    market = analyze_market()
    learning = learn_patterns()
    outcomes = get_outcomes()

    recommendations = []

    # מוצר
    if market["competitors_tracked"] > 0:
        recommendations.append(
            "לנתח יתרון תחרותי ולא להתחרות רק ביכולות AI כלליות"
        )

    # לקוחות
    if learning["total_interactions"] > 0:
        recommendations.append(
            "להמשיך ניסויי משתמשים ולבנות החלטות מתוך ראיות"
        )
    else:
        recommendations.append(
            "לבצע ניסוי ראשון עם משתמשים אמיתיים"
        )

    # שלב חברה
    if context.get("stage") == "prototype":
        recommendations.append(
            "להתמקד בהוכחת ערך לפני הרחבת יכולות"
        )

    return {
        "question": question,
        "company_context": context,
        "competitive_state": market,
        "customer_learning": learning,
        "past_outcomes": outcomes,
        "recommendations": recommendations,
        "generated_at": time.time()
    }
