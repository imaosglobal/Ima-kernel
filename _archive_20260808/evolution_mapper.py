import json
from pathlib import Path
from datetime import datetime


BASE=Path.home()/"ima_kernel"

SOURCE=BASE/".ima/evolution/git_history_memory.jsonl"

TARGET=BASE/".ima/evolution/evolution_map.json"


def load():

    items=[]

    if SOURCE.exists():

        for line in SOURCE.read_text().splitlines():

            try:
                items.append(
                    json.loads(line)
                )
            except:
                pass

    return items


def map_history():

    events=load()


    eras={

        "kernel":[
            "kernel",
            "runtime",
            "system"
        ],

        "memory_learning":[
            "memory",
            "learning",
            "brain"
        ],

        "product":[
            "saas",
            "app",
            "ui"
        ]

    }


    result={

        "generated":
        datetime.now().isoformat(),

        "eras":{},


        "future_questions":[

            "what capability is missing?",

            "what can be compressed?",

            "what should connect next?"

        ]

    }


    for era,keys in eras.items():

        found=[]

        for e in events:

            text=e["event"].lower()

            if any(
                k in text
                for k in keys
            ):
                found.append(
                    e["event"]
                )


        result["eras"][era]={
            "count":len(found),
            "examples":found[:10]
        }


    TARGET.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":

    map_history()

    print(
        "EVOLUTION MAP CREATED"
    )
