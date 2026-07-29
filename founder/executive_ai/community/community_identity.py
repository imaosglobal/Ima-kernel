from pathlib import Path
import json

FILE = Path("founder/data/community_identity.json")

def create_identity(name, platform="internal"):

    identity = {
        "community_id": name.lower().replace(" ","_"),
        "platform": platform,
        "members": 0,
        "trust_score": 0
    }

    FILE.parent.mkdir(parents=True, exist_ok=True)

    data=[]
    if FILE.exists():
        data=json.loads(FILE.read_text())

    data.append(identity)

    FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return identity


def get_identities():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
