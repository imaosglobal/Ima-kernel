def synthesize(memories):

    if not memories:
        return {
            "summary":"אין מספיק מידע בזיכרון"
        }

    points=[]

    for item in memories:

        memory=item.get("memory",{})

        text=(
            memory.get("answer")
            or memory.get("text")
            or memory.get("question")
            or ""
        )

        if text:
            points.append(text)

    return {
        "summary":"\n".join(points),
        "sources":len(points)
    }
