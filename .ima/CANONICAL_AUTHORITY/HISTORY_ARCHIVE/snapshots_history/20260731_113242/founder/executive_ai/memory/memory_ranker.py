import time


def rank_memories(memories, query):

    ranked=[]

    query_words=set(
        str(query).lower().split()
    )

    for memory in memories:

        text=" ".join([
            str(memory.get("question","")),
            str(memory.get("answer","")),
            str(memory.get("text",""))
        ]).lower()

        words=set(text.split())

        relevance=len(
            query_words.intersection(words)
        )

        importance=memory.get(
            "importance",
            0
        )

        score=relevance + importance

        ranked.append({
            "memory":memory,
            "score":score
        })

    ranked.sort(
        key=lambda x:x["score"],
        reverse=True
    )

    return ranked[:5]
