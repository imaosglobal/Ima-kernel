from pathlib import Path
import json

files = {

"founder/executive_ai/community/production/audit_log.py": '''
from pathlib import Path
import json,time

FILE=Path("founder/data/audit_log.json")

def record(event,data):

    logs=[]

    if FILE.exists():
        logs=json.loads(FILE.read_text())

    logs.append({
        "time":time.time(),
        "event":event,
        "data":data
    })

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(
            logs,
            indent=2,
            ensure_ascii=False
        )
    )

    return logs[-1]
''',

"founder/executive_ai/community/production/api_gateway.py": '''
TOKENS={}

def register_app(name,token):

    TOKENS[token]={
        "name":name,
        "active":True
    }

    return TOKENS[token]


def authorize(token):

    return TOKENS.get(token,{
        "active":False
    })
''',

"founder/executive_ai/community/production/version_control.py": '''
from pathlib import Path
import json,time

FILE=Path("founder/data/community_versions.json")


def create_version(component,change):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "id":time.time(),
        "component":component,
        "change":change
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(data,indent=2)
    )

    return item
''',

"IMA_PUBLIC_STRUCTURE.md": '''
# IMA Public Repository Structure

IMA/
|
├── community/
|   ├── connectors
|   ├── documentation
|   ├── examples
|
├── developer/
|   ├── api
|   ├── sdk
|
├── governance/
|   ├── rules
|   ├── license
|
└── PRIVATE_CORE
    └── protected
''',

"IMA_DEPLOYMENT_CHECKLIST.md": '''
# IMA Deployment Checklist

[x] Community gateway
[x] Security layer
[x] Validation pipeline
[x] CRM bridge

Next:

[ ] Real OAuth connectors
[ ] Cloud deployment
[ ] Public repository
[ ] Developer portal
[ ] Legal review
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


