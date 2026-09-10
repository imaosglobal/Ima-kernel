import json
from pathlib import Path

# 1. Canonical creator identity
founder_file = Path("product/identity/founder_registry.json")
data = json.loads(founder_file.read_text(encoding="utf-8"))

founder = data.setdefault("founder", {})

founder.update({
    "id": "creator_001",
    "name": "Ori Cohen",
    "role": "founder_and_creator",
    "roles": [
        "founder",
        "creator",
        "architect",
        "poet",
        "songwriter"
    ],
    "canonical": True,
    "same_person_identity": True
})

data["identity_statement"] = (
    "Ori Cohen is the Founder, Creator, Architect, Poet and Songwriter of IMA. "
    "Founder and Creator refer to the same person."
)

data["creator_sources"] = {
    "facebook": {
        "url": "https://www.facebook.com/share/1FFdWxZt2a/",
        "owner_id": "creator_001",
        "owner": "Ori Cohen",
        "type": "creator_content_source",
        "content_types": [
            "poetry",
            "songs",
            "lyrics",
            "posts",
            "ideas",
            "creative_writing",
            "media"
        ],
        "learning_enabled": True,
        "continuous_scan": True,
        "canonical_source": True,
        "read_only": True
    }
}

founder_file.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# 2. Founder context
context_file = Path("founder/data/founder_context.json")
context = json.loads(context_file.read_text(encoding="utf-8"))

context["founder_id"] = "creator_001"
context["founder_name"] = "Ori Cohen"
context["founder_is_creator"] = True
context["creator_is_founder"] = True

context["creator_profile"] = {
    "id": "creator_001",
    "name": "Ori Cohen",
    "roles": [
        "founder",
        "creator",
        "architect",
        "poet",
        "songwriter"
    ],
    "system": "IMA",
    "canonical": True
}

context["creator_sources"] = {
    "facebook": {
        "url": "https://www.facebook.com/share/1FFdWxZt2a/",
        "enabled": True,
        "continuous_scan": True,
        "learning_enabled": True,
        "read_only": True
    }
}

context_file.write_text(
    json.dumps(context, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# 3. Canonical learning registry
registry_file = Path("learning/sources/registry.json")
registry = json.loads(registry_file.read_text(encoding="utf-8"))

sources = registry.setdefault("sources", [])

facebook = {
    "name": "Ori Cohen — Facebook Creator Source",
    "module": "learning.sources.ori_facebook",
    "function": "search",
    "priority": 95,
    "enabled": True,
    "trust": "high"
}

sources = [
    s for s in sources
    if s.get("name") != facebook["name"]
]

sources.append(facebook)
registry["sources"] = sources

registry_file.write_text(
    json.dumps(registry, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("CREATOR PROFILE CONNECTED")
print("Creator: Ori Cohen")
print("ID: creator_001")
print("Roles: founder, creator, architect, poet, songwriter")
print("Facebook source: CONNECTED")
print("Learning: ENABLED")
print("Continuous scan: ENABLED")
