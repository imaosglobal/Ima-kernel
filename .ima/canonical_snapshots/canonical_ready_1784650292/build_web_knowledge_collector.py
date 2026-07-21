from pathlib import Path
import json
import time
import urllib.request
import urllib.parse

base=Path("learning")
base.mkdir(exist_ok=True)

p=base/"web_knowledge_collector.py"

p.write_text(r'''
import urllib.request
import urllib.parse
import json


def normalize(q):
    return (
        q.replace("מה זה ","")
        .replace("מהי ","")
        .replace("?","")
        .strip()
    )


def wikidata(q):
    try:
        term=urllib.parse.quote(normalize(q))
        url=(
            "https://www.wikidata.org/w/api.php?"
            "action=wbsearchentities&search="
            +term+
            "&language=he&format=json"
        )

        req=urllib.request.Request(
            url,
            headers={
                "User-Agent":"IMA-Knowledge-Agent/1.0"
            }
        )

        data=json.loads(
            urllib.request.urlopen(req,timeout=8)
            .read()
            .decode("utf8")
        )

        items=data.get("search",[])

        if items:
            x=items[0]
            return {
                "content":x.get("description","") or x.get("label",""),
                "source":"Wikidata",
                "url":"https://www.wikidata.org/wiki/"+x.get("id",""),
                "confidence":0.8
            }

    except Exception:
        pass

    return None


def wikipedia(q):
    try:
        term=urllib.parse.quote(normalize(q))

        url=(
            "https://he.wikipedia.org/w/api.php?"
            "action=query&prop=extracts"
            "&exintro=true&explaintext=true"
            "&format=json&titles="
            +term
        )

        req=urllib.request.Request(
            url,
            headers={
                "User-Agent":"IMA-Knowledge-Agent/1.0"
            }
        )

        data=json.loads(
            urllib.request.urlopen(req,timeout=8)
            .read()
            .decode("utf8")
        )

        pages=data.get("query",{}).get("pages",{})

        for _,page in pages.items():
            if "extract" in page:
                return {
                    "content":page["extract"][:1000],
                    "source":"Wikipedia",
                    "url":"https://he.wikipedia.org/wiki/"+normalize(q),
                    "confidence":0.85
                }

    except Exception:
        pass

    return None


def collect_sources(question):

    results=[]

    for fn in [
        wikipedia,
        wikidata
    ]:
        r=fn(question)
        if r:
            results.append(r)

    return sorted(
        results,
        key=lambda x:x.get("confidence",0),
        reverse=True
    )


def best_answer(question):

    results=collect_sources(question)

    if results:
        return results[0]

    return None
''',
encoding="utf8"
)

Path(".ima/web_knowledge_collector.lock").write_text(
json.dumps(
{
"state":"CREATED",
"sources":["Wikipedia","Wikidata"],
"time":time.time()
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)

print("WEB KNOWLEDGE COLLECTOR CREATED")
