
import json
import urllib.request

CONFIG={
    "sources":[
        "local",
        "wikipedia"
    ]
}


def local_search(question):
    try:
        data=json.loads(open("learning/world_knowledge.json",encoding="utf8").read())
        if question in data or ("מה זה "+question) in data:
            key = question if question in data else "מה זה "+question
            return {
                "content":data[key]["content"],
                "source":"local",
                "confidence":data[question].get("confidence",0.8)
            }
    except Exception:
        pass
    return None


def wikipedia_search(question):
    try:
        
term=question.replace("מה זה ","").strip()

url="https://he.wikipedia.org/api/rest_v1/page/summary/"+term.replace(" ","_")

        req=urllib.request.Request(
            url,
            headers={"User-Agent":"IMA-Knowledge-Agent"}
        )
        with urllib.request.urlopen(req,timeout=5) as r:
            data=json.loads(r.read().decode("utf8"))

        if data.get("extract"):
            return {
                "content":data["extract"],
                "source":"wikipedia",
                "confidence":0.85
            }

    except Exception:
        pass

    return None


def get_real_source(question):

    for source in CONFIG["sources"]:

        if source=="local":
            result=local_search(question)

        elif source=="wikipedia":
            result=wikipedia_search(question)

        else:
            result=None

        if result:
            return result

    return None
