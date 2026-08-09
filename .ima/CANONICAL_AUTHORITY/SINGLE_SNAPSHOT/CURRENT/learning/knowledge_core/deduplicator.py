
def clean_duplicates(items):
    seen=set()
    result=[]

    for x in items:
        key=x.get("content","")[:200]

        if key not in seen:
            seen.add(key)
            result.append(x)

    return result
