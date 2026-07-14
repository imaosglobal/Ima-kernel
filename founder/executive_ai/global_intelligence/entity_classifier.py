from founder.executive_ai.global_intelligence.entity_types import ENTITY_TYPES


def classify_entity(entity):

    text=str(entity).lower()

    scores={}

    for entity_type,data in ENTITY_TYPES.items():

        score=0

        for signal in data["signals"]:
            if signal.lower() in text:
                score+=1

        scores[entity_type]=score

    return max(
        scores,
        key=scores.get
    )
