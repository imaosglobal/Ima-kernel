import json
from pathlib import Path


FILES=[
    Path("founder/data/decisions.json"),
    Path("founder/data/outcomes.json")
]


def build_timeline():

    events=[]

    for file in FILES:

        if file.exists():

            try:
                data=json.loads(
                    file.read_text()
                )

                events.extend(data)

            except Exception:
                pass

    events.sort(
        key=lambda x:x.get("time",0)
    )

    return events
