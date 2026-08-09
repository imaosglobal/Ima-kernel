def accept_lesson(lesson):

    if lesson.get("validated") is True:
        return {
            "status": "accepted",
            "lesson": lesson
        }

    return {
        "status": "rejected",
        "reason": "not_validated"
    }
