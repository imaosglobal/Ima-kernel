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
