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
