
from learning.source_manager import get_real_source
import urllib.request
import json

SOURCES = [
    "local",
    "wikidata",
    "wikipedia",
    "duckduckgo",
    "crossref",
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


def wikidata_search(question):

    try:
        term=normalize(question)

        url=(
            "https://www.wikidata.org/w/api.php?"
            "action=wbsearchentities"
            "&search="
            + term.replace(" ","%20")
            +
            "&language=he"
            "&format=json"
        )

        req=urllib.request.Request(
            url,
            headers={
                "User-Agent":"IMA-Knowledge-Agent/1.0"
            }
        )

        with urllib.request.urlopen(req,timeout=8) as r:
            data=json.loads(
                r.read().decode("utf8")
            )

        results=data.get("search",[])

        if results:
            item=results[0]

            return {
                "content":item.get(
                    "description",
                    item.get("label","")
                ),
                "source":"Wikidata",
                "url":
                "https://www.wikidata.org/wiki/"
                +
                item.get("id",""),
                "confidence":0.8
            }

    except Exception:
        pass

    return None



def get_best_source(question):

    # 1. Local
    local=get_real_source(question)

    if local:
        return {
            **local,
            "url":local.get("url","")
        }


    # 2. Wikidata
    wiki=wikidata_search(question)

    if wiki:
        return wiki


    return None
