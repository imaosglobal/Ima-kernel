from pathlib import Path
import json
import time

FILE=Path("founder/data/community_expansion.json")


def load():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return {
        "communities":[],
        "connectors":[],
        "events":[]
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


def create_community(name,platform):

    data=load()

    item={
        "id":name.lower().replace(" ","_"),
        "name":name,
        "platform":platform,
        "status":"active",
        "created":time.time()
    }

    data["communities"].append(item)

    save(data)

    return item


def register_connector(name,category):

    data=load()

    connector={
        "name":name,
        "category":category,
        "status":"ready"
    }

    data["connectors"].append(connector)

    save(data)

    return connector


def record_event(source,event):

    data=load()

    data["events"].append({
        "source":source,
        "event":event,
        "time":time.time()
    })

    save(data)

    return data["events"][-1]
