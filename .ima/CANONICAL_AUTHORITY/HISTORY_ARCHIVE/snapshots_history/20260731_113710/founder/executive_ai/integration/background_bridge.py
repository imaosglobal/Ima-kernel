from founder.executive_ai.integration.relevance_detector import is_founder_relevant
from founder.executive_ai.advisor.founder_advisor import advise


def process_background(message):

    result = is_founder_relevant(message)

    if result["relevant"]:

        strategy = advise(message)

        return {
            "founder_ai": True,
            "signals": result["signals"],
            "strategy": strategy
        }

    return {
        "founder_ai": False,
        "signals": []
    }
