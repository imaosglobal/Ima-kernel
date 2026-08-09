from founder.executive_ai.competitive_intelligence.strategy_engine import generate_strategy
from founder.executive_ai.decision_memory import save_decision


def advise(question):

    strategy = generate_strategy(question)

    save_decision(strategy)

    return strategy
