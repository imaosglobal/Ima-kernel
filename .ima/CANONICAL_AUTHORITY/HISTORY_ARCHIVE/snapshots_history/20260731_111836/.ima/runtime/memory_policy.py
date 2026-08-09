from datetime import datetime


def classify(event_type, data):
    if event_type in ["identity", "goal", "decision"]:
        return "long_term"

    if event_type in ["learning", "conversation_v2"]:
        return "adaptive"

    return "short_term"


def importance(event_type, data):
    score = 1

    if event_type in ["identity", "goal", "decision"]:
        score += 5

    if isinstance(data, dict):
        text = str(data)

        if len(text) > 100:
            score += 1

        keywords = [
            "IMA",
            "memory",
            "learning",
            "truth",
            "system"
        ]

        for k in keywords:
            if k.lower() in text.lower():
                score += 1

    return score


def evaluate(event_type, data):
    return {
        "type": classify(event_type, data),
        "importance": importance(event_type, data),
        "created": datetime.utcnow().isoformat()
    }
