
def score_answer(item):
    score=0

    score+=item.get("confidence",0)

    source=item.get("source","")

    if source in ["Wikipedia","Nature","NASA","PubMed"]:
        score+=1

    return score
