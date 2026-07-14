from founder.executive_ai.global_intelligence.entity_classifier import classify_entity
from founder.executive_ai.global_intelligence.opportunity_memory import save_entity


def scan_entities(items):

    results=[]

    for item in items:

        entity={
            "name":item,
            "type":classify_entity(item)
        }

        save_entity(entity)

        results.append(entity)

    return results
