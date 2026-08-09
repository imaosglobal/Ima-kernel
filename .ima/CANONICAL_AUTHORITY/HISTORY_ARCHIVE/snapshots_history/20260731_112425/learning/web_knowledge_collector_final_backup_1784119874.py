
from learning.sources.html_extractor import extract_text
import json
import time
import urllib.request
import urllib.parse


ALIASES = {
    "איינשטיין": "אלברט איינשטיין",
    "einstein": "Albert Einstein",
    "קוואנטום": "מכניקת הקוונטים",
}


def normalize(q):
    q=q.strip()
    q=q.replace("מה זה ","")
    q=q.replace("מהי ","")
    q=q.replace("?","")
    return ALIASES.get(q.lower(),q)



def local_source(q):
    try:
        with open(
            "learning/world_knowledge.json",
            encoding="utf8"
        ) as f:
            data=json.load(f)

        term=normalize(q)

        for k in [q,term]:
            if k in data:
                return {
                    "content":data[k]["content"],
                    "source":"IMA Memory",
                    "url":"",
                    "confidence":0.7
                }

    except:
        pass

    return None



def wikipedia_source(q):

    try:
        term=urllib.parse.quote(normalize(q))

        url=(
            "https://he.wikipedia.org/w/api.php?"
            "action=query&prop=extracts"
            "&exintro=true"
            "&explaintext=true"
            "&format=json"
            "&titles="+term
        )

        req=urllib.request.Request(
            url,
            headers={
                "User-Agent":"IMA Knowledge Engine"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=8
        ) as r:

            data=json.loads(
                r.read().decode("utf8")
            )


        pages=data.get(
            "query",
            {}
        ).get(
            "pages",
            {}
        )


        for page in pages.values():

            text=page.get(
                "extract",
                ""
            )

            if text:

                return {
                    "content":text,
                    "source":"Wikipedia",
                    "url":
                    "https://he.wikipedia.org/wiki/"
                    +
                    urllib.parse.quote(normalize(q)),
                    "confidence":0.9
                }

    except:
        pass

    return None



def duckduckgo_source(q):

    try:

        term=urllib.parse.quote(
            normalize(q)
        )

        url=(
            "https://api.duckduckgo.com/"
            "?q="+term+
            "&format=json"
        )


        with urllib.request.urlopen(
            url,
            timeout=8
        ) as r:

            data=json.loads(
                r.read().decode("utf8")
            )


        text=data.get(
            "AbstractText",
            ""
        )


        if text:

            return {
                "content":text,
                "source":"DuckDuckGo",
                "url":data.get(
                    "AbstractURL",
                    ""
                ),
                "confidence":0.75
            }


    except:
        pass

    return None




def collect_sources(question):

    results=[]

    for source in [
        local_source,
        wikipedia_source,
        duckduckgo_source
    ]:

        r=source(question)

        if r:

            r["retrieved_at"]=time.time()

            results.append(r)


    return results




def rank(result):

    source=result.get(
        "source",
        ""
    )

    text=result.get(
        "content",
        ""
    )


    score=result.get(
        "confidence",
        0
    )


    if source=="Wikipedia":
        score+=0.5

    if source=="DuckDuckGo":
        score+=0.3

    if source=="IMA Memory":
        score+=0.1


    if len(text)>500:
        score+=0.2


    return score




def best_answer(question):

    results=collect_sources(question)


    if not results:
        return None


    results.sort(
        key=rank,
        reverse=True
    )


    return results[0]

