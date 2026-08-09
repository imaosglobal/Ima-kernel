from pathlib import Path

files = {

"founder/executive_ai/community/community_manager.py": '''
from pathlib import Path
import json
import time

FILE=Path("founder/data/community_v2.json")


def load():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return {
        "communities":[],
        "members":[],
        "roles":[]
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


def create(name, category):

    data=load()

    item={
        "id":name.lower().replace(" ","_"),
        "name":name,
        "category":category,
        "created":time.time()
    }

    data["communities"].append(item)

    save(data)

    return item
''',


"founder/executive_ai/community/developer_profile.py": '''
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
''',


"founder/executive_ai/community/role_engine.py": '''
def role_from_trust(score):

    if score >= 80:
        return "core_maintainer"

    if score >= 50:
        return "reviewer"

    if score >= 20:
        return "contributor"

    return "member"
''',


"founder/executive_ai/community/trust_v2.py": '''
def calculate(profile):

    score=0

    score += profile.get(
        "contributions",
        0
    ) * 5

    score += profile.get(
        "validated_lessons",
        0
    ) * 10

    return min(score,100)
''',


"founder/executive_ai/community/permission_engine.py": '''
def permissions(role):

    table={

        "member":[
            "read"
        ],

        "contributor":[
            "read",
            "submit"
        ],

        "reviewer":[
            "read",
            "submit",
            "review"
        ],

        "core_maintainer":[
            "read",
            "submit",
            "review",
            "approve"
        ]

    }

    return table.get(
        role,
        []
    )
'''
}


for p,c in files.items():

    path=Path(p)
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        c.strip()+"\n",
        encoding="utf8"
    )


print("IMA COMMUNITY EXPANSION V2 CREATED")
