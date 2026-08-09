from pathlib import Path

files = {

"founder/executive_ai/community/community_identity.py": '''
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
''',

"founder/executive_ai/community/community_crm.py": '''
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
''',

"founder/executive_ai/community/trust_engine.py": '''
def calculate_trust(member):

    score=0

    score += member.get("accepted_lessons",0)*10
    score += member.get("contributions",0)*2

    return min(score,100)
''',

"founder/executive_ai/community/sandbox_runner.py": '''
def test_contribution(change):

    return {
        "status":"sandbox_pass",
        "change":change
    }
''',

"founder/executive_ai/community/connector_manager.py": '''
CONNECTORS={}


def register_connector(name,handler):

    CONNECTORS[name]=handler


def list_connectors():

    return list(CONNECTORS.keys())
''',

"founder/executive_ai/community/community_growth.py": '''
def analyze_growth():

    return {
        "status":"growth_engine_active",
        "communities_found":0,
        "recommendations":[]
    }
'''
}


for path,content in files.items():

    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)

    if not p.exists():
        p.write_text(
            content.strip()+"\n",
            encoding="utf8"
        )


print("IMA COMMUNITY ECOSYSTEM CREATED")
