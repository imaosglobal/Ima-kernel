def calculate(profile):

    score=0

    score += profile.get(
        "contributions",
        0
    ) * 5

    score += profile.get(
        "validated_lessons",
        0
    ) * 10

    return min(score,100)
