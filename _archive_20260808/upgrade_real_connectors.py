from pathlib import Path

files = {

"founder/executive_ai/community/security/vault.py": '''
from pathlib import Path
import json

FILE=Path("founder/data/community_secrets.json")


def save_secret(service,key):

    data={}

    if FILE.exists():
        data=json.loads(FILE.read_text())

    data[service]={
        "key":key,
        "enabled":True
    }

    FILE.parent.mkdir(parents=True,exist_ok=True)

    FILE.write_text(
        json.dumps(data,indent=2)
    )


def get_secret(service):

    if FILE.exists():
        return json.loads(FILE.read_text()).get(service)

    return None
''',


"founder/executive_ai/community/connectors/base_connector.py": '''
class BaseConnector:

    name="base"

    def fetch(self):

        return []

    def normalize(self,item):

        return {
            "source":self.name,
            "content":item
        }
''',


"founder/executive_ai/community/connectors/github_connector.py": '''
from .base_connector import BaseConnector


class GithubConnector(BaseConnector):

    name="github"

    def fetch(self):

        return []

    def receive_webhook(self,event):

        return {
            "source":"github",
            "type":"contribution",
            "content":event
        }
''',


"founder/executive_ai/community/connectors/discord_connector.py": '''
from .base_connector import BaseConnector


class DiscordConnector(BaseConnector):

    name="discord"

    def fetch(self):

        return []

    def receive_event(self,event):

        return {
            "source":"discord",
            "type":"community_signal",
            "content":event
        }
''',


"founder/executive_ai/community/connector_gateway.py": '''
from founder.executive_ai.community.connectors.github_connector import GithubConnector
from founder.executive_ai.community.connectors.discord_connector import DiscordConnector


CONNECTORS={
    "github":GithubConnector(),
    "discord":DiscordConnector()
}


def ingest(source,data):

    connector=CONNECTORS.get(source)

    if not connector:
        return {
            "status":"unknown_source"
        }

    return connector.normalize(data)


def available():

    return list(CONNECTORS.keys())
''',


"founder/executive_ai/community/community_api_policy.py": '''
POLICY={

"external_can":
[
"submit_lessons",
"send_feedback",
"propose_changes"
],

"external_cannot":
[
"modify_core",
"write_private_memory",
"change_identity"
]

}


def get_policy():

    return POLICY
'''
}


for p,c in files.items():

    path=Path(p)
    path.parent.mkdir(parents=True,exist_ok=True)

    if not path.exists():
        path.write_text(
            c.strip()+"\n",
            encoding="utf8"
        )


