from founder.executive_ai.memory.learning_feedback import get_feedback
from founder.executive_ai.memory.lesson_mapper import map_lesson_to_signals
from founder.executive_ai.knowledge.concept_graph import expand_signal


def collect_learning_signals():

    feedback=get_feedback()

    signals=[]

    for item in feedback:

        mapped = map_lesson_to_signals(
            item.get("lesson","")
        )

        for signal in mapped:
            signals.append(signal)
            signals.extend(
                expand_signal(signal)
            )

    return list(set(signals))


def adapt_recommendations(recommendations):

    learned_signals = collect_learning_signals()

    adapted=[]

    for rec in recommendations:

        score=1
        text=rec.lower()

        if (
            ("משתמש" in text or "ניסוי" in text)
            and (
                "user_outreach" in learned_signals
                or "user_testing" in learned_signals
            )
        ):
            score+=3

        if (
            "לקוחות" in text
            and "customers" in learned_signals
        ):
            score+=2

        if (
            "שיפור מוצר" in text
            and "product_improvement" in learned_signals
        ):
            score+=2

        adapted.append({
            "recommendation":rec,
            "priority":score,
            "learning_basis":learned_signals
        })

    adapted.sort(
        key=lambda x:x["priority"],
        reverse=True
    )

    return adapted
