from pathlib import Path

files = {

"founder/executive_ai/community/crm_trust_bridge.py": '''
from founder.executive_ai.community.unified_crm import load, save
from founder.executive_ai.community.trust_engine import calculate_trust


def update_member_trust(member_id):

    data = load()

    for member in data["people"]:

        if member["id"] == member_id:

            member["trust"] = calculate_trust(member)

            save(data)

            return member

    return {
        "status":"member_not_found"
    }
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


