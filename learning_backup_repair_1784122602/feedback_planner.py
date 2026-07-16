from learning.feedback_engine import process_feedback
from learning.improvement_planner import build_improvement_plan
from learning.knowledge_dedup import remove_duplicates


def generate_feedback_improvements():

    feedback = process_feedback()

    suggestions = []

    for item in feedback:

        if item == "needs_improvement":
            suggestions.append(
                "לשפר פעולה שקיבלה דירוג נמוך"
            )

        if item == "successful_pattern":
            suggestions.append(
                "לשמר ולחזק דפוס פעולה מוצלח"
            )

    unique = remove_duplicates(
        [{"lesson": x} for x in suggestions],
        key="lesson"
    )

    cleaned_suggestions = [
        x["lesson"]
        for x in unique
    ]

    return build_improvement_plan(cleaned_suggestions)
