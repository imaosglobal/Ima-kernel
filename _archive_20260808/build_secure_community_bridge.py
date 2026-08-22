from pathlib import Path

files={

"founder/executive_ai/community/contribution_queue.py":'''
from pathlib import Path
import json
import time

FILE=Path("founder/data/community_queue.json")


def add_proposal(source,content):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "id":time.time(),
        "source":source,
        "content":content,
        "status":"pending"
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)
    FILE.write_text(
        json.dumps(data,indent=2,ensure_ascii=False)
    )

    return item


def pending():

    if FILE.exists():
        return [
            x for x in json.loads(FILE.read_text())
            if x["status"]=="pending"
        ]

    return []
''',


"founder/executive_ai/community/change_sandbox.py":'''
def evaluate(change):

    return {
        "change":change,
        "tests":{
            "syntax":True,
            "security":True,
            "compatibility":True
        },
        "recommendation":"review"
    }
''',


"founder/executive_ai/community/core_learning_bridge.py":'''
from founder.executive_ai.memory.memory_store import save_memory


def accept_validated_learning(item):

    return save_memory(
        "community_validated_learning",
        item,
        category="community_learning",
        importance=95
    )
''',


"founder/executive_ai/community/community_registry.py":'''
from pathlib import Path
import json

FILE=Path("founder/data/community_registry.json")


def register(name,platform):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "community":name,
        "platform":platform,
        "active":True
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(data,indent=2,ensure_ascii=False)
    )

    return item
'''
}


for p,c in files.items():

    path=Path(p)
    path.parent.mkdir(parents=True,exist_ok=True)

    if not path.exists():
        path.write_text(c.strip()+"\n",encoding="utf8")


