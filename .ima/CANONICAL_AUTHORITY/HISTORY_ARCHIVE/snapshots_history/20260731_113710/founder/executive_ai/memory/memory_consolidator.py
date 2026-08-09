from collections import defaultdict


def consolidate(events):

    groups=defaultdict(list)

    for event in events:

        key=(
            event.get("question")
            or event.get("action")
            or "general"
        )

        groups[key].append(event)


    result=[]

    for key,items in groups.items():

        latest=max(
            items,
            key=lambda x:x.get("time",0)
        )

        result.append({
            "topic":key,
            "occurrences":len(items),
            "latest":latest
        })

    result.sort(
        key=lambda x:x["latest"].get("time",0),
        reverse=True
    )

    return result
