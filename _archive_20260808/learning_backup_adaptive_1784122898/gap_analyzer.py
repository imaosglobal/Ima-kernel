from learning.knowledge_gaps import get_gaps
from learning.self_reflection import suggest_improvement


def analyze_gaps():

    gaps = get_gaps()

    topics = {}

    for gap in gaps:
        question = gap.get("question", "")

        if "תודעה" in question:
            topic = "consciousness"
        elif "פיזיקה" in question:
            topic = "physics"
        elif "רגש" in question:
            topic = "emotion"
        elif "בינה" in question:
            topic = "artificial_intelligence"
        else:
            topic = "general"

        topics[topic] = topics.get(topic, 0) + 1


    for topic, count in topics.items():
        suggest_improvement(
            "knowledge_gap",
            f"להרחיב ידע בתחום {topic} ({count} שאלות חסרות)"
        )


    return topics
