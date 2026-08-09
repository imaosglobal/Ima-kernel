from founder.executive_ai.community.community_event_router import route_event


ROUTES = {}


def register_route(name, handler):

    ROUTES[name] = handler


def receive_message(
    platform,
    user,
    message
):

    return route_event(
        platform,
        user,
        message
    )


def available_routes():

    return list(ROUTES.keys())


def gateway_status():

    return {

        "name":
        "IMA Community API Gateway",

        "routes":
        available_routes(),

        "status":
        "online"

    }
