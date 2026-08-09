STATE={}

def update_state(data=None):

    if data:
        STATE.update(data)

    return STATE
