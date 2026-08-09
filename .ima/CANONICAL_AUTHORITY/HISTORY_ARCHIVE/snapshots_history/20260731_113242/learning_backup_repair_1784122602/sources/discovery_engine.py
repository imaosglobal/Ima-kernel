import time
import json
from pathlib import Path


CANDIDATES = Path(
    "learning/sources/candidates.json"
)


def save_candidate(candidate):

    if CANDIDATES.exists():
        data=json.loads(
            CANDIDATES.read_text(
                encoding="utf8"
            )
        )
    else:
        data=[]


    for item in data:
        if (
            item.get("name")==candidate.get("name")
            and
            item.get("url")==candidate.get("url")
        ):
            return item


    candidate["discovered_at"]=time.time()

    data.append(candidate)

    CANDIDATES.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    return candidate


def discover_url(name,url,category):

    return save_candidate(
        {
            "name":name,
            "url":url,
            "category":category,
            "status":"pending",
            "trusted":False
        }
    )
