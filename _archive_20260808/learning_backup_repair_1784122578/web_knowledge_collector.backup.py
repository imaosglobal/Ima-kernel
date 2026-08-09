import time
import urllib.request
import urllib.parse
import json


SOURCES = [
    "local",
    "wikipedia",
    "duckduckgo",
    "arxiv"
]


def normalize(question):
    return (
        question
        .replace("מה זה ","")
        .replace("מהי ","")
        .replace("?","")
        .strip()
    )


def local_source(question):
    try:
        with open(
            "learning/world_knowledge.json",
            encoding="utf8"
        ) as f:
            data=json.load(f)

        for key in [
            question,
            normalize(question)
        ]:
            if key in data:
                return {
                    "content":data[key]["content"],
                    "source":"IMA Memory",
                    "url":"",
                    "confidence":0.95
                }

    except:
        pass

    return None



def wikipedia_source(question):

    try:
        term=urllib.parse.quote(normalize(question))

        url=(
            "https://he.wikipedia.org/w/api.php?"
            "action=query&prop=extracts"
            "&exintro=true"
            "&explaintext=true"
            "&format=json"
            "&titles="
            +term
        )

        req=urllib.request.Request(
            url,
            headers={
                "User-Agent":"IMA Knowledge Engine"
            }
        )

        with urllib.request.urlopen(req,timeout=8) as r:

            data=json.loads(
                r.read().decode("utf8")
            )

        pages=data.get("query",{}).get("pages",{})

        for page in pages.values():

            text=page.get("extract","")

            if text:

                return {
                    "content":text,
                    "source":"Wikipedia",
                    "url":
                    "https://he.wikipedia.org/wiki/"
                    +normalize(question),
                    "confidence":0.90
                }

    except:
        pass

    return None



def duckduckgo_source(question):

    try:

        q=urllib.parse.quote(normalize(question))

        url=(
            "https://api.duckduckgo.com/"
            "?q="+q+
            "&format=json"
        )

        with urllib.request.urlopen(
            url,
            timeout=8
        ) as r:

            data=json.loads(
                r.read().decode("utf8")
            )

        text=data.get("AbstractText","")

        if text:

            return {
                "content":text,
                "source":"DuckDuckGo",
                "url":data.get("AbstractURL",""),
                "confidence":0.75
            }

    except:
        pass

    return None



def collect_sources(question):

    results=[]

    for fn in [
        local_source,
        wikipedia_source,
        duckduckgo_source
    ]:

        r=fn(question)

        if r:
            r["retrieved_at"]=time.time()
            results.append(r)


    return results



def rank_source(result):

    score=result.get("confidence",0)

    if len(result.get("content",""))>200:
        score+=0.1

    if result.get("url"):
        score+=0.05

    return score



def best_answer(question):

    results=collect_sources(question)

    if not results:
        return None

    results.sort(
        key=rank_source,
        reverse=True
    )

    return results[0]
