from pathlib import Path

files = {

"founder/executive_ai/community/integration_registry.py": '''
from pathlib import Path
import json

FILE=Path("founder/data/integration_registry.json")


def register(name,category,status="planned"):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "name":name,
        "category":category,
        "status":status
    }

    data.append(item)

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

    return item


def list_integrations():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
''',


"founder/executive_ai/community/core_sync_manager.py": '''
from founder.executive_ai.community.unified_crm import load


def system_status():

    crm=load()

    return {
        "crm_people":len(crm.get("people",[])),
        "communities":len(crm.get("communities",[])),
        "contributions":len(crm.get("contributions",[])),
        "status":"synchronized"
    }
''',


"founder/executive_ai/community/community_expansion_manifest.py": '''
MANIFEST={

"name":"IMA Global Community Expansion",

"future_connectors":[

"GitHub",
"Telegram",
"WhatsApp",
"Discord",
"Slack",
"IEEE",
"Research Networks",
"Developer Platforms"

],

"languages":[

"he",
"en",
"ar",
"es",
"fr",
"de",
"zh",
"ja",
"hi",
"ru"

],

"policy":"validated_growth_only"

}


def get_manifest():

    return MANIFEST
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


print("IMA INTEGRATION CONSOLIDATION CREATED")
