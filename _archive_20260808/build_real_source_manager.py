from pathlib import Path
import json
import time
import urllib.request

base=Path("learning")
base.mkdir(exist_ok=True)

source_file=base/"source_manager.py"

source_file.write_text(r'''
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
        if question in data:
            return {
                "content":data[question]["content"],
                "source":"local",
                "confidence":data[question].get("confidence",0.8)
            }
    except Exception:
        pass
    return None


def wikipedia_search(question):
    try:
        url="https://he.wikipedia.org/api/rest_v1/page/summary/"+question.replace(" ","_")
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
''',encoding="utf8")


Path(".ima/real_source_manager.lock").write_text(
json.dumps({
"state":"CREATED",
"sources":["local","wikipedia"],
"time":time.time()
},ensure_ascii=False,indent=2),
encoding="utf8"
)

print("REAL SOURCE MANAGER CREATED")
