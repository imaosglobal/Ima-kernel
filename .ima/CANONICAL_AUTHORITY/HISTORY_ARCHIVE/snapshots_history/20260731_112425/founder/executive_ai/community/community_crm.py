from pathlib import Path
import json

FILE=Path("founder/data/community_crm.json")


def add_member(member, community):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "member":member,
        "community":community,
        "contributions":0,
        "accepted_lessons":0,
        "trust":0
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return item


def get_members():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
