from pathlib import Path
import json

FILE=Path("founder/data/developer_profiles.json")


def create_profile(user_id,name):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    profile={
        "id":user_id,
        "name":name,
        "trust":0,
        "contributions":0,
        "role":"member"
    }

    data.append(profile)

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )

    return profile
