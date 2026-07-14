from founder.executive_ai.memory.learning_feedback import get_feedback


def optimize_recommendations(recommendations):

    feedback = get_feedback()

    lessons=[]

    for item in feedback:
        lessons.append(
            {
                "from_action": item.get("action"),
                "lesson": item.get("lesson"),
                "result": item.get("result")
            }
        )

    return {
        "recommendations": recommendations,
        "learned_lessons": lessons,
        "feedback_count": len(feedback)
    }
