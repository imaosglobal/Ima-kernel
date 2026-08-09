from learning.lesson_memory import get_lessons


def retrieve_relevant_lessons(
    context=None,
    limit=5,
):
    """
    Read-only lesson retrieval.

    Matches current observations/goals against stored lesson text.
    No writes.
    No execution.
    """

    context = context or {}

    observations = context.get("observations", [])
    goals = context.get("goals", [])

    if not isinstance(observations, list):
        observations = [observations]

    if not isinstance(goals, list):
        goals = [goals]

    query_terms = set()

    for item in observations + goals:
        if item:
            query_terms.update(
                str(item).lower().split()
            )

    lessons = get_lessons(limit=100)

    ranked = []

    for lesson in lessons:
        searchable = " ".join([
            str(lesson.get("plan_status", "")),
            str(lesson.get("evaluation_status", "")),
            str(lesson.get("feedback_overall", "")),
            str(lesson.get("feedback", "")),
        ]).lower()

        score = sum(
            1
            for term in query_terms
            if term and term in searchable
        )

        ranked.append({
            "lesson": lesson,
            "relevance_score": score,
        })

    ranked.sort(
        key=lambda item: item["relevance_score"],
        reverse=True,
    )

    return {
        "query_terms": sorted(query_terms),
        "matches": ranked[:limit],
        "status": "lessons_retrieved",
        "execution": "disabled",
    }
