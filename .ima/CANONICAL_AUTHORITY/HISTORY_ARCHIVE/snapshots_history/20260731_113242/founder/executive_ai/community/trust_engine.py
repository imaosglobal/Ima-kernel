def calculate_trust(member):

    score=0

    score += member.get("accepted_lessons",0)*10
    score += member.get("contributions",0)*2

    return min(score,100)
