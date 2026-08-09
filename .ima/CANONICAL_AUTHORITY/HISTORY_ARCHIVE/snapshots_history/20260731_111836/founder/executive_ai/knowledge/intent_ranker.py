from founder.executive_ai.knowledge.intent_mapper import detect_intents


PRIORITY={
    "user_testing":3,
    "product_improvement":3,
    "customers":2,
    "competitive_learning":2
}


def rank_intents(text):

    intents=detect_intents(text)

    ranked=[]

    for intent in intents:
        ranked.append({
            "intent":intent,
            "importance":PRIORITY.get(intent,1)
        })

    ranked.sort(
        key=lambda x:x["importance"],
        reverse=True
    )

    return ranked
