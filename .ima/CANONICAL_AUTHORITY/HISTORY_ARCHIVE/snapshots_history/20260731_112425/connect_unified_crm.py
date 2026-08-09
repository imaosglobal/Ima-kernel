from pathlib import Path
import json
import time

files={

"founder/executive_ai/community/unified_crm.py":'''
from pathlib import Path
import json

FILE=Path("founder/data/ima_unified_crm.json")


def load():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return {
        "people":[],
        "communities":[],
        "contributions":[]
    }


def save(data):

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


def link_person(identity, source="community"):

    data=load()

    for p in data["people"]:
        if p["id"]==identity["id"]:
            return p

    person={
        "id":identity["id"],
        "name":identity.get("name"),
        "source":source,
        "trust":0,
        "contributions":0
    }

    data["people"].append(person)

    save(data)

    return person


def add_contribution(person_id, contribution):

    data=load()

    item={
        "person":person_id,
        "content":contribution,
        "timestamp":time.time()
    }

    data["contributions"].append(item)

    for p in data["people"]:
        if p["id"]==person_id:
            p["contributions"]+=1
            p["trust"]=min(
                100,
                p["trust"]+2
            )

    save(data)

    return item
''',


"founder/executive_ai/community/crm_bridge.py":'''
from founder.executive_ai.community.unified_crm import (
    link_person,
    add_contribution
)


def sync_community_member(identity, contribution):

    person=link_person(identity)

    add_contribution(
        person["id"],
        contribution
    )

    return {
        "status":"synced",
        "person":person
    }
'''
}


for p,c in files.items():

    path=Path(p)
    path.parent.mkdir(parents=True,exist_ok=True)

    if not path.exists():
        path.write_text(
            c.strip()+"\n",
            encoding="utf8"
        )


print("UNIFIED CRM CONNECTOR CREATED")
