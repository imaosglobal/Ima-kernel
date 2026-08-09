import json
import re
from pathlib import Path
from datetime import datetime


BASE=Path.home()/"ima_kernel"

SOURCE=BASE/".ima/evolution/git_history_memory.jsonl"

TARGET=BASE/".ima/evolution/capability_memory.json"


def load():

    result=[]

    if SOURCE.exists():

        for line in SOURCE.read_text().splitlines():

            try:
                result.append(json.loads(line))
            except:
                pass

    return result



def normalize(text):

    text=text.lower()

    remove=[
        "add",
        "fix",
        "create",
        "update",
        "stable",
        "ima"
    ]

    for x in remove:
        text=text.replace(x,"")

    text=re.sub(
        r'[^a-z0-9 ]',
        '',
        text
    )

    return "_".join(
        text.split()[:5]
    )



def extract():

    events=load()

    capabilities={}


    for e in events:

        name=normalize(
            e["event"]
        )

        if not name:
            continue


        if name not in capabilities:

            capabilities[name]={
                "first_seen":e["date"],
                "sources":[],
                "confidence":0.5
            }


        capabilities[name]["sources"].append(
            e["commit"]
        )

        count=len(
            capabilities[name]["sources"]
        )

        capabilities[name]["confidence"]=min(
            0.95,
            0.5+(count*0.05)
        )


    output={

        "generated":
        datetime.now().isoformat(),

        "capabilities":
        capabilities

    }


    TARGET.write_text(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":

    extract()

    print(
        "CAPABILITIES EXTRACTED"
    )
