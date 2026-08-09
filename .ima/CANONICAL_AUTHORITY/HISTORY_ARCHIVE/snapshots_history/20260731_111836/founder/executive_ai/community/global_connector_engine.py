CONNECTORS={}


def register_platform(name, connector):

    CONNECTORS[name]=connector


def receive_message(platform, user, message):

    connector=CONNECTORS.get(platform)

    if not connector:
        return {
            "status":"platform_not_connected",
            "platform":platform
        }

    return connector.handle(
        user,
        message
    )


def platforms():

    return list(CONNECTORS.keys())
