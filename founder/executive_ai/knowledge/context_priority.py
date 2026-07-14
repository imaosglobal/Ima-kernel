STAGE_PRIORITY={

    "prototype":{
        "customers":5,
        "user_testing":4,
        "product_improvement":3,
        "competitive_learning":2
    },

    "growth":{
        "customers":3,
        "product_improvement":5,
        "competitive_learning":4
    },

    "scale":{
        "competitive_learning":5,
        "product_improvement":4,
        "customers":3
    }
}


def prioritize_by_stage(intents, stage):

    priorities=STAGE_PRIORITY.get(stage,{})

    ranked=[]

    for item in intents:
        intent=item["intent"]

        ranked.append({
            "intent":intent,
            "importance":priorities.get(
                intent,
                item["importance"]
            )
        })

    ranked.sort(
        key=lambda x:x["importance"],
        reverse=True
    )

    return ranked
