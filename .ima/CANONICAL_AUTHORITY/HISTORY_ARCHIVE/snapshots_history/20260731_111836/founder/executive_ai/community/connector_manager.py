CONNECTORS={}


def register_connector(name,handler):

    CONNECTORS[name]=handler


def list_connectors():

    return list(CONNECTORS.keys())
