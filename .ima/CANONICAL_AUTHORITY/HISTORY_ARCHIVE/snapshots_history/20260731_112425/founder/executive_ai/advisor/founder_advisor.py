from founder.executive_ai.customer_intelligence.market_learning import learn_patterns
from founder.executive_ai.competitive_intelligence.strategy_engine import generate_strategy
from founder.executive_ai.decision_memory import save_decision
from founder.executive_ai.knowledge.intent_ranker import rank_intents
from founder.executive_ai.knowledge.context_priority import prioritize_by_stage
from founder.executive_ai.memory.decision_insight import generate_insights
from founder.executive_ai.memory.learning_optimizer import optimize_recommendations


def advise(question):

    intents = rank_intents(question)

    stage='prototype'
    intents = prioritize_by_stage(intents, stage)

    stage='prototype'
    intents = prioritize_by_stage(intents, stage)

    strategy = generate_strategy(question)

    insights = generate_insights()

    learning = optimize_recommendations(
        strategy.get(
            "recommendations",
            []
        )
    )

    result={
        "question": question,
        "intents": intents,
        "primary_intent": intents[0] if intents else None,
        "strategy": strategy,
        "memory_insights": insights,
        "learning": learning
    }

    save_decision(result)

    return result
