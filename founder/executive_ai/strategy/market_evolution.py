import json
from pathlib import Path
import time

FILE=Path("founder/data/market_models.json")


def create_market_model(problem,solution):

    model={
        "created":time.time(),
        "problem":problem,
        "solution":solution,
        "customers":{
            "first":"early adopters עם כאב ברור",
            "hundred":"קהילות ונישות עם צורך חוזר",
            "thousand":"עסקים קטנים וארגונים",
            "million":"פלטפורמה גלובלית"
        },
        "expansion_questions":[
            "מי מרוויח הכי הרבה מהפתרון?",
            "מי משלם הכי מהר?",
            "מי מפיץ את המוצר לאחרים?"
        ]
    }

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    data.append(model)

    FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return model


def latest():
    if FILE.exists():
        return json.loads(FILE.read_text())[-1]

    return None
