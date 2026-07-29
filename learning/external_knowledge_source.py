import urllib.request
import urllib.parse
import json

from learning.source_registry import get_sources


def fetch_external(question):

    providers = [
        fetch_wikidata,
        fetch_wikipedia,
        fetch_openalex,
        fetch_arxiv,
        fetch_openlibrary,
    ]

    for provider in providers:
        try:
            result = provider(question)

            if result and result.get("content"):
                result["provider"] = provider.__name__
                return result

        except Exception:
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
        headers={"User-Agent":"IMA-Knowledge-Engine"}
    )

    with urllib.request.urlopen(req,timeout=10) as r:
        data=json.loads(r.read().decode("utf8"))

    if "extract" not in data:
        return None

    return {
        "content":data["extract"],
        "domain":"encyclopedia",
        "source":"wikipedia"
    }



def fetch_wikidata(question):

    q=urllib.parse.quote(question)

    url=(
        "https://www.wikidata.org/w/api.php?"
        "action=wbsearchentities&search="
        +q+
        "&language=en&format=json"
    )

    with urllib.request.urlopen(url,timeout=10) as r:
        data=json.loads(r.read().decode("utf8"))

    if not data.get("search"):
        return None

    item=data["search"][0]

    return {
        "content":item.get("description",""),
        "domain":"knowledge_graph",
        "source":"wikidata"
    }



def fetch_openalex(question):

    q=urllib.parse.quote(question)

    url=(
        "https://api.openalex.org/works?search="
        +q+
        "&per-page=1"
    )

    with urllib.request.urlopen(url,timeout=10) as r:
        data=json.loads(r.read().decode("utf8"))

    if not data.get("results"):
        return None

    work=data["results"][0]

    return {
        "content":work.get("title",""),
        "domain":"research",
        "source":"openalex",
        "id":work.get("id")
    }



def fetch_arxiv(question):

    q=urllib.parse.quote(question)

    url=(
        "http://export.arxiv.org/api/query?"
        "search_query=all:"
        +q+
        "&max_results=1"
    )

    with urllib.request.urlopen(url,timeout=10) as r:
        text=r.read().decode("utf8")

    if "<title>" not in text:
        return None

    title=text.split("<title>")[2].split("</title>")[0]

    return {
        "content":title,
        "domain":"scientific_papers",
        "source":"arxiv"
    }



def fetch_openlibrary(question):

    q=urllib.parse.quote(question)

    url=(
        "https://openlibrary.org/search.json?q="
        +q+
        "&limit=1"
    )

    with urllib.request.urlopen(url,timeout=10) as r:
        data=json.loads(r.read().decode("utf8"))

    docs=data.get("docs")

    if not docs:
        return None

    return {
        "content":docs[0].get("title",""),
        "domain":"books",
        "source":"openlibrary"
    }
