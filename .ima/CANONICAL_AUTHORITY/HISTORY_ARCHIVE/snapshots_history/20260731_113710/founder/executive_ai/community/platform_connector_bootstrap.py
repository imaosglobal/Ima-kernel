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
