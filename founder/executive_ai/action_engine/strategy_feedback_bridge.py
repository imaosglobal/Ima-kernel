from founder.executive_ai.action_engine.feedback_engine import analyze_feedback


def apply_feedback_to_strategy(strategy):

    feedback = analyze_feedback()

    lessons = feedback.get(
        "lessons",
        []
    )

    adjustments=[]

    for lesson in lessons:

        if "government" in lesson.lower():
            adjustments.append(
                "להדגיש השפעה ציבורית וערך חברתי בפניות לממשלה"
            )

        if "message" in lesson.lower():
            adjustments.append(
                "לשפר התאמת מסר לפי סוג גוף"
            )


    return {
        "original_strategy":strategy,
        "feedback_lessons":lessons,
        "adjustments":adjustments
    }
