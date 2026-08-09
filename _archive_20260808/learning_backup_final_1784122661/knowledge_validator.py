
def validate(data):
    if not data:
        return False,0

    if "content" in data and len(data["content"])>10:
        return True,0.9

    return False,0.1
