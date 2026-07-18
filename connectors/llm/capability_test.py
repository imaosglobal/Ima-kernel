import subprocess
import time


def inspect_model(model):

    result={
        "model":model,
        "score":0,
        "tested":False,
        "reason":""
    }

    try:
        out=subprocess.check_output(
            ["ollama","show",model],
            timeout=5,
            text=True,
            stderr=subprocess.DEVNULL
        )

        result["tested"]=True

        # דירוג שמרני לפי גודל בלבד
        if "7B" in out or "7.2B" in out:
            result["score"]=70
        elif "3B" in out or "3.8B" in out:
            result["score"]=80
        elif "1B" in out:
            result["score"]=60
        else:
            result["score"]=50

    except Exception as e:
        result["reason"]=str(e)

    return result


def rank(models):

    results=[
        inspect_model(m)
        for m in models
    ]

    return sorted(
        results,
        key=lambda x:x["score"],
        reverse=True
    )
