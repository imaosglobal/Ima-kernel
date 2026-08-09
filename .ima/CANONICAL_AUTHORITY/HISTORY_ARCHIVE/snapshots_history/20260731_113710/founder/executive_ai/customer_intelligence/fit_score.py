def calculate_fit(profile):

    score=0
    reasons=[]

    signals=" ".join(profile.get("signals",[])).lower()

    if "ai" in signals:
        score+=30
        reasons.append("AI company")

    if profile.get("stage") in [
        "pre-seed",
        "seed"
    ]:
        score+=20
        reasons.append("early stage")

    if profile.get("founders",0)<=5:
        score+=20
        reasons.append("small team")

    if "llm" in signals or "agent" in signals:
        score+=30
        reasons.append("high memory need")

    return {
        "company":profile["name"],
        "ima_fit_score":score,
        "reasons":reasons
    }
