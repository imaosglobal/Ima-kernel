
import json
from pathlib import Path

FILE = Path("founder/data/action_feedback.json")


def analyze_feedback():

    lessons=[]
    records=[]

    if FILE.exists():
        records=json.loads(FILE.read_text())

    for item in records:

        if item.get("lesson"):
            lessons.append(item["lesson"])

        if item.get("status")=="no_response":
            target=item.get("target","")
            lessons.append(
                f"{target}: outreach failed, improve message"
            )

        if item.get("status")=="outreach_ready":

            lessons.append(
                f"{item.get('target')}: outreach prepared, not confirmed success"
            )

    return {
        "total":len(records),
        "lessons":lessons,
        "records":records
    }


def deduplicate_records(records):

    seen=set()
    clean=[]

    for r in records:

        key=(
            str(r.get("target")),
            str(r.get("status")),
            str(r.get("score"))
        )

        if key not in seen:
            seen.add(key)
            clean.append(r)

    return clean

