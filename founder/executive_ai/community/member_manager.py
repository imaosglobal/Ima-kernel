from pathlib import Path
import json
import time

FILE = Path("founder/data/community_members.json")


def load_members():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return []


def save_members(data):

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def get_member(member_id):

    members = load_members()

    for member in members:
        if member["id"] == member_id:
            return member

    return None


def create_member(member_id, name, platform):

    existing = get_member(member_id)

    if existing:
        return existing

    member = {

        "id": member_id,
        "name": name,
        "platform": platform,

        "trust": 0,

        "contributions": 0,

        "validated_lessons": 0,

        "role": "member",

        "created": time.time(),

        "history": []

    }

    members = load_members()

    members.append(member)

    save_members(members)

    return member


def update_activity(member_id, action, validated=False):

    members = load_members()

    for member in members:

        if member["id"] == member_id:

            member["contributions"] += 1

            if validated:
                member["validated_lessons"] += 1


            member["history"].append({

                "action": action,

                "time": time.time()

            })


            member["trust"] = min(
                100,
                member["contributions"] * 5 +
                member["validated_lessons"] * 10
            )


            save_members(members)

            return member


    return None
