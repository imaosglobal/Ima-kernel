
from learning.sources.html_extractor import extract_text
import urllib.request
import urllib.parse
import json


SOURCES=[
    "wikipedia",
    "wikidata"
]


def normalize(q):
    return (
        q.replace("מה זה ","")
        .replace("מהי ","")
        .replace("?","")
        .strip()
    )


def wikipedia(term):

    try:
        url=(
        "https://he.wikipedia.org/w/api.php?"
        "action=query&prop=extracts"
        "&exintro=true"
        "&explaintext=true"
        "&format=json&titles="
        +urllib.parse.quote(term)
        )

        req=urllib.request.Request(
            url,
            headers={
            "User-Agent":"IMA Knowledge Engine"
            }
        )

        with urllib.request.urlopen(req,timeout=10) as r:
            data=json.loads(r.read())

        pages=data["query"]["pages"]

        for page in pages.values():
            if "extract" in page:
                return {
                "content":page["extract"],
                "source":"Wikipedia",
                "url":
                "https://he.wikipedia.org/wiki/"
                +urllib.parse.quote(term),
                "confidence":0.85
                }

    except Exception:
        pass

    return None



def wikidata(term):

    try:
        url=(
        "https://www.wikidata.org/w/api.php?"
        "action=wbsearchentities&language=he"
        "&format=json&search="
        +urllib.parse.quote(term)
        )

        with urllib.request.urlopen(url,timeout=10) as r:
            data=json.loads(r.read())

        if data.get("search"):

            x=data["search"][0]

            return {
            "content":
            x.get("description",
            x.get("label","")),
            "source":"Wikidata",
            "url":
            "https://www.wikidata.org/wiki/"
            +x["id"],
            "confidence":0.75
            }

    except Exception:
        pass

    return None



def search_web_knowledge(question):

    term=normalize(question)

    for fn in [
        wikipedia,
        wikidata
    ]:
        result=fn(term)

        if result:
            return result

    return None
