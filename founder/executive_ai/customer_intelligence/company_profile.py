import json
import time
from pathlib import Path

FILE=Path("founder/data/customers/company_profiles.json")


def create_company(
    name,
    industry,
    stage,
    founders,
    signals
):

    profile={
        "name":name,
        "industry":industry,
        "stage":stage,
        "founders":founders,
        "signals":signals,
        "created":time.time()
    }

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    data.append(profile)

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return profile
