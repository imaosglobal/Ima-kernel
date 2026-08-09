from pathlib import Path

files = {

"founder/executive_ai/community/identity_verification.py": '''
from pathlib import Path
import json

FILE=Path("founder/data/identity_registry.json")


def load():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []


def register(identity_id,name):

    data=load()

    item={
        "id":identity_id,
        "name":name,
        "verified":True
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


def verify(identity_id):

    for item in load():

        if item["id"]==identity_id:
            return True

    return False
''',


"founder/executive_ai/community/conversation_memory.py": '''
from pathlib import Path
import json
import time

FILE=Path("founder/data/conversation_memory.json")


def save_message(user,message):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    event={
        "user":user,
        "message":message,
        "time":time.time()
    }

    data.append(event)

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

    return event


def history():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []
''',


"founder/executive_ai/community/conversation_engine.py": '''
from founder.executive_ai.community.conversation_memory import save_message


def respond(user,message):

    save_message(
        user,
        message
    )

    return {

        "user":user,

        "response":
        "IMA received your message: " + message,

        "status":
        "processed"

    }
''',


"founder/executive_ai/community/response_router.py": '''
from founder.executive_ai.community.conversation_engine import respond


def route(user,message):

    return respond(
        user,
        message
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


print("IMA CONVERSATION GATEWAY + IDENTITY LAYER CREATED")
