from pathlib import Path
import json
import time

FILE=Path("founder/data/trust_graph.json")


def load():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return {
        "nodes":[],
        "relations":[]
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


def add_member(member):

    data=load()

    data["nodes"].append({
        "type":"person",
        "id":member["id"],
        "name":member["name"],
        "trust":member.get("trust",0),
        "created":time.time()
    })

    save(data)

    return member


def connect(person,community):

    data=load()

    data["relations"].append({
        "from":person,
        "to":community,
        "type":"member_of"
    })

    save(data)

    return {
        "status":"connected",
        "from":person,
        "to":community
    }
