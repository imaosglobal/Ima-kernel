
def entity_bonus(question,text):

    q=question.lower()
    t=text.lower()

    if "who was" in q or "who is" in q:
        if "einstein" in t:
            return 20
        if "biography" in t:
            return 20
        return -10

    return 0
