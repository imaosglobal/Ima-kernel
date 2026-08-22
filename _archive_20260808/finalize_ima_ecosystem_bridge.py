from pathlib import Path

files = {

"founder/executive_ai/community/platform_connector_bootstrap.py": '''
from founder.executive_ai.community.global_connector_engine import register_platform
from founder.executive_ai.community.connectors.chat_connector import ChatConnector


def initialize_connectors():

    platforms = [
        "telegram",
        "whatsapp",
        "discord",
        "github"
    ]

    for p in platforms:
        register_platform(
            p,
            ChatConnector(p)
        )

    return {
        "status":"connectors_initialized",
        "platforms":platforms
    }
''',


"founder/executive_ai/community/community_dashboard.py": '''
from founder.executive_ai.community.platform_registry import list_platforms
from founder.executive_ai.community.global_connector_engine import platforms


def status():

    return {

        "registered_platforms":
            list_platforms(),

        "active_connectors":
            platforms(),

        "status":
            "community_network_online"

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



