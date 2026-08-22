from pathlib import Path

files = {

"founder/executive_ai/community/crm_event_bridge.py": '''
from founder.executive_ai.community.unified_crm import (
    link_person,
    add_contribution
)


def process_community_event(
    user_id,
    name,
    source,
    contribution
):

    identity={
        "id":user_id,
        "name":name
    }

    person=link_person(
        identity,
        source
    )

    event=add_contribution(
        user_id,
        contribution
    )

    return {
        "status":"crm_updated",
        "person":person,
        "event":event
    }
''',


"founder/executive_ai/community/trust_sync.py": '''
from founder.executive_ai.community.unified_crm import load


def calculate_community_health():

    data=load()

    return {

        "members":
            len(data.get("people",[])),

        "contributions":
            len(data.get("contributions",[])),

        "status":
            "active"

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


