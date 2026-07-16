from learning.source_quality_ranker import rank

from learning.sources.html_extractor import extract_text
import time


def weighted_score(source):

    name=source.get("source","")
    trust=source.get("trust_score",70)

    return rank(name,trust)


def fuse_sources(question, sources):
    if not sources:
        return None

    ranked=[]

    for s in sources:
        content=s.get("content","").strip()

        if "<html" in content.lower() or "<link" in content.lower() or "<meta" in content.lower():
            content=extract_text(content)

        bad=[
            "apple-touch-icon",
            "viewport",
            "charset",
            "stylesheet",
            "<link"
        ]

        if any(x in content.lower() for x in bad):
            continue

        if len(content)<50:
            continue

        score=s.get("confidence",0)

        source=s.get("source","")

        if source in ["Nature","NASA","PubMed","arXiv","MIT"]:
            score+=2

        if len(content)>300:
            score+=0.5

        ranked.append({
            "content":content,
            "source":source,
            "url":s.get("url",""),
            "confidence":score
        })

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
