def validate_lesson(lesson):

    if not isinstance(lesson, dict):
        return False

    return bool(
        lesson.get("lesson")
    )
