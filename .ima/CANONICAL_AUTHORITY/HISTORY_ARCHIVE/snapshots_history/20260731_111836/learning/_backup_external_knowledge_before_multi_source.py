import urllib.request
import urllib.parse
import json

from learning.source_registry import get_sources


def fetch_external(question):

    providers = [
        fetch_wikipedia,
        fetch_wikidata,
        fetch_arxiv,
        fetch_openalex
    ]

    for provider in providers:
        try:
            result = provider(question)
            if result:
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
    return None



def fetch_arxiv(question):
    return None



def fetch_openalex(question):
    return None
