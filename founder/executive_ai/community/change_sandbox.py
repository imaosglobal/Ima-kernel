def evaluate(change):

    return {
        "change":change,
        "tests":{
            "syntax":True,
            "security":True,
            "compatibility":True
        },
        "recommendation":"review"
    }
