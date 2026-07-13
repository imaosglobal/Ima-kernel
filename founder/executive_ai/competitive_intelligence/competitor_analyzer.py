from founder.executive_ai.competitive_intelligence.competitor_memory import get_competitors


def analyze_market():

    competitors=get_competitors()

    lessons=[]

    for c in competitors:
        lessons.extend(
            c.get("lessons_for_ima",[])
        )

    return {
        "competitors_tracked":len(competitors),
        "market_lessons":list(set(lessons))
    }
