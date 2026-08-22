import json
from pathlib import Path

HOME=Path.home()

GRAPH=HOME/".ima/memory/universal_knowledge_graph.json"


def load_graph():
    try:
        return json.loads(GRAPH.read_text(encoding="utf-8"))
    except:
        return {}


def interpret(topic):

    data=load_graph()
    results=[]

    words=topic.lower().split()

    for domain,items in data.get("domains",{}).items():
        if any(w in domain.lower() for w in words):

            results.append(
                f"{domain} מחובר לידע על {', '.join(items) if isinstance(items,list) else items}"
            )

            for relation,value in data.get("relations",{}).items():
                if domain in relation:

                    if isinstance(value,dict):
                        meaning=value.get("type","")
                    else:
                        meaning=value

                    results.append(
                        f"הקשר שנמצא: {relation} → {meaning}"
                    )


    return results


if __name__=="__main__":
    import sys
    for x in interpret(" ".join(sys.argv[1:])):
