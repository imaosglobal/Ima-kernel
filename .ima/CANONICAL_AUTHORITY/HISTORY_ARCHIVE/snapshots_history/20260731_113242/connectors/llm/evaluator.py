
def evaluate(results):
    if not results:
        return ""

    for k,v in results.items():
        if v and not v.startswith("["):
            return v

    return ""
