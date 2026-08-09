def rank_leads(leads):

    ranked=[]

    for lead in leads:

        score=lead.get(
            "ima_fit_score",
            0
        )

        ranked.append({
            "company":lead["company"],
            "priority":
                "A" if score>=80 else
                "B" if score>=50 else
                "C",
            "score":score,
            "reasons":lead.get(
                "reasons",
                []
            )
        })

    return sorted(
        ranked,
        key=lambda x:x["score"],
        reverse=True
    )
