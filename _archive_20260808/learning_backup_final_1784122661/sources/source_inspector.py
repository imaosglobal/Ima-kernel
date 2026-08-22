import urllib.request
import urllib.error
import time


def inspect_candidate(candidate):

    result = candidate.copy()

    score = 0

    url = candidate.get("url","")


    if url.startswith("https://"):
        score += 20


    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent":"IMA Source Inspector"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=5
        ) as r:

            if r.status == 200:
                score += 40
            elif r.status in [301,302,403]:
                score += 20

    except urllib.error.HTTPError as e:
        if e.code in [301,302,403]:
            score += 20
        else:
            score -= 10

    except Exception:
        score -= 10


    category = candidate.get(
        "category",
        ""
    )


    if category in [
        "medical",
        "science",
        "research"
    ]:
        score += 20


    result["trust_score"]=score
    result["checked_at"]=time.time()


    if score >= 60:
        result["status"]="approved"
        result["trusted"]=True
    else:
        result["status"]="review"


    return result
