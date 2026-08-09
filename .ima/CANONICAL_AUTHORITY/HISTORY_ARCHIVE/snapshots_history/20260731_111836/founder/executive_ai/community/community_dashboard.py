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
