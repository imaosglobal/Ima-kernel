from founder.executive_ai.community.community_expansion_engine import load


def health():

    data=load()

    return {

        "communities":
        len(data["communities"]),

        "connectors":
        len(data["connectors"]),

        "events":
        len(data["events"]),

        "status":
        "expansion_ready"

    }
