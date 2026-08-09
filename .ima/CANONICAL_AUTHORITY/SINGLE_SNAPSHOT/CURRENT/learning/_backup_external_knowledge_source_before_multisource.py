import urllib.request
import urllib.parse
import json

from learning.source_registry import get_sources


def fetch_external(question):

    providers = [
        fetch_wikidata,
        fetch_wikipedia,
        fetch_openalex,
        fetch_arxiv
    ]

    for provider in providers:
        try:
            result = provider(question)

            if result:
                result["provider"] = provider.__name__
                return result

        except Exception as e:
            continue

    return None



def fetch_wikipedia(question):

    q = urllib.parse.quote(question)

    url = (
        "https://he.wikipedia.org/api/rest_v1/page/summary/"
        + q
    )

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent":"IMA-Knowledge-Engine/1.0"
        }
    )

    with urllib.request.urlopen(req,timeout=10) as r:
        data=json.loads(
            r.read().decode("utf8")
        )

    if "extract" not in data:
        return None

    return {
        "content":data["extract"],
        "domain":"general",
        "source":"wikipedia"
    }



def fetch_wikidata(question):

    q = urllib.parse.quote(question)

    url=(
        "https://www.wikidata.org/w/api.php?"
        "action=wbsearchentities&search="
        + q +
        "&language=he&format=json"
    )

    with urllib.request.urlopen(url,timeout=10) as r:
        data=json.loads(
            r.read().decode("utf8")
        )

    if not data.get("search"):
        return None

    item=data["search"][0]

    return {
        "content":item.get("description",""),
        "domain":"knowledge_graph",
        "source":"wikidata",
        "id":item.get("id")
    }



def fetch_openalex(question):

    q=urllib.parse.quote(question)

    url=(
        "https://api.openalex.org/works?search="
        + q +
        "&per-page=1"
    )

    with urllib.request.urlopen(url,timeout=10) as r:
        data=json.loads(
            r.read().decode("utf8")
        )

    results=data.get("results")

    if not results:
        return None

    work=results[0]

    return {
        "content":work.get("title",""),
        "domain":"research",
        "source":"openalex",
        "id":work.get("id")
    }



def fetch_arxiv(question):

    return None
