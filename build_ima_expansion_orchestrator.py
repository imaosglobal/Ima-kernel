from pathlib import Path

files = {

"founder/executive_ai/community/expansion_orchestrator.py": '''
from founder.executive_ai.community.global_connector_engine import receive_message
from founder.executive_ai.community.contribution_queue import add_proposal
from founder.executive_ai.community.change_sandbox import evaluate
from founder.executive_ai.community.core_learning_bridge import accept_validated_learning
from founder.executive_ai.community.crm_bridge import sync_community_member


def process_external_signal(platform, user, message):

    incoming = receive_message(
        platform,
        user,
        message
    )

    proposal = add_proposal(
        platform,
        message
    )

    analysis = evaluate(
        proposal
    )

    return {
        "incoming": incoming,
        "proposal": proposal,
        "sandbox": analysis,
        "status": "awaiting_validation"
    }


def promote_learning(proposal):

    proposal["status"]="validated"

    return accept_validated_learning(
        proposal
    )
''',


"founder/executive_ai/community/platform_registry.py": '''
from pathlib import Path
import json

FILE=Path(
"founder/data/platform_registry.json"
)


def register_platform(name,category):

    data=[]

    if FILE.exists():
        data=json.loads(
            FILE.read_text()
        )

    item={
        "name":name,
        "category":category,
        "active":True
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


def list_platforms():

    if FILE.exists():
        return json.loads(
            FILE.read_text()
        )

    return []
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


print("IMA EXPANSION ORCHESTRATOR CREATED")
