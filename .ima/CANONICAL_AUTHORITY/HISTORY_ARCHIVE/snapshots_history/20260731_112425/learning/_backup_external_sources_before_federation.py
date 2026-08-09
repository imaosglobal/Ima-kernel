import urllib.request
import urllib.parse
import json


def fetch_external(question):

    sources = [
        fetch_wikipedia,
    ]

    for source in sources:
        try:
            result = source(question)
            if result:
                return result
        except Exception:
            continue

    return None



def fetch_wikipedia(question):

    query = urllib.parse.quote(question)

    url = (
        "https://he.wikipedia.org/api/rest_v1/page/summary/"
        + query
    )

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "IMA-Knowledge-Engine/1.0"
        }
    )

    with urllib.request.urlopen(req, timeout=10) as r:
        data=json.loads(r.read().decode("utf8"))

    if "extract" not in data:
        return None

    return {
        "content": data["extract"],
        "domain": "general",
        "source": "wikipedia",
        "url": data.get("content_urls",{})
    }
