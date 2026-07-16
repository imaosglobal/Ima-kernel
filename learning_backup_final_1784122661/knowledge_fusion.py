import time


def fuse_sources(question, sources):

    if not sources:
        return None

    ranked=[]

    for s in sources:

        content=s.get("content","").strip()

        if len(content)<20:
            continue

        score=s.get("confidence",0)

        source=s.get("source","")

        if source=="Wikipedia":
            score+=1.0

        elif source=="DuckDuckGo":
            score+=0.7

        elif source=="IMA Memory":
            score+=0.5

        if len(content)>500:
            score+=0.2

        ranked.append(
            {
                "content":content,
                "source":source,
                "url":s.get("url",""),
                "confidence":score,
                "retrieved_at":time.time()
            }
        )


    if not ranked:
        return None


    ranked.sort(
        key=lambda x:x["confidence"],
        reverse=True
    )


    return {
        "answer":ranked[0]["content"],
        "source":ranked[0]["source"],
        "url":ranked[0]["url"],
        "confidence":ranked[0]["confidence"],
        "all_sources":ranked
    }
