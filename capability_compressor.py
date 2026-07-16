import json
from pathlib import Path
from datetime import datetime


BASE=Path.home()/"ima_kernel"

SOURCE=BASE/".ima/evolution/capability_memory.json"

TARGET=BASE/".ima/evolution/system_capabilities.json"


RULES={

"memory":[
    "memory",
    "pattern",
    "learning",
    "brain"
],

"kernel":[
    "kernel",
    "runtime",
    "system",
    "module"
],

"interface":[
    "ui",
    "client",
    "app",
    "frontend"
],

"automation":[
    "auto",
    "pipeline",
    "builder",
    "deploy"
],

"knowledge":[
    "knowledge",
    "reason",
    "graph",
    "analysis"
]

}


def load():

    if SOURCE.exists():

        return json.loads(
            SOURCE.read_text()
        )

    return {"capabilities":{}}



def compress():

    data=load()

    output={

        "generated":
        datetime.now().isoformat(),

        "capabilities":{}

    }


    for name,value in data["capabilities"].items():

        domain="general"

        text=name.lower()

        for d,keys in RULES.items():

            if any(
                k in text
                for k in keys
            ):
                domain=d
                break


        if domain not in output["capabilities"]:

            output["capabilities"][domain]={
                "count":0,
                "confidence":0,
                "sources":[]
            }


        item=output["capabilities"][domain]

        item["count"]+=1

        item["sources"].append(
            name
        )


        item["confidence"]=round(
            min(
                0.95,
                0.5+
                item["count"]/100
            ),
            2
        )


    TARGET.write_text(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":

    compress()

    print(
        "CAPABILITY COMPRESSION COMPLETE"
    )
