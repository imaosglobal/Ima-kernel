
import json
import time
from pathlib import Path

FILE=Path("founder/data/market_models.json")


def create_market_model(problem,solution):

    model={
        "created":time.time(),
        "problem":problem,
        "solution":solution,
        "growth_path":[
            "early adopters",
            "communities",
            "small businesses",
            "enterprise",
            "global platform"
        ],
        "questions":[
            "who pays fastest?",
            "who has strongest pain?",
            "who spreads adoption?"
        ]
    }

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    data.append(model)

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return model


def latest():

    if FILE.exists():
        return json.loads(FILE.read_text())[-1]

    return None
