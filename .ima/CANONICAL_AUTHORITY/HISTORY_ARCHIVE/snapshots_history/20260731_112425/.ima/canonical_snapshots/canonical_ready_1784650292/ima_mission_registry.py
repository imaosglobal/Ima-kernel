from pathlib import Path
import json
import time

GOV = Path(".ima/governance")
GOV.mkdir(parents=True, exist_ok=True)

MISSION = {
    "system": "IMA",
    "state": "MISSION_LOCKED",
    "created": time.time(),

    "mission": {
        "primary": "להיות מערכת עוזרת חכמה, בטוחה ואנושית לכל אדם בכל שלב בחיים",
        "vision": "ללוות ילדים ומבוגרים בלמידה, יצירה, תמיכה וניהול ידע אישי",
        "scope": [
            "children",
            "families",
            "education",
            "personal_assistance",
            "robots",
            "mobile_devices",
            "future_interfaces"
        ]
    },

    "principles": [
        "human_first",
        "safety_first",
        "privacy_by_design",
        "single_brain_architecture",
        "transparent_learning",
        "no_duplicate_core_systems"
    ],

    "forbidden_changes": [
        "replace_canonical_brain",
        "create_duplicate_orchestrator",
        "bypass_governance"
    ],

    "architecture": {
        "brain": "learning/meta_orchestrator.py",
        "orchestrator": "learning/meta_orchestrator.py",
        "governance": ".ima/governance"
    }
}

path = GOV / "mission_registry.json"

path.write_text(
    json.dumps(MISSION, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("=== IMA MISSION REGISTRY ===")
print("CREATED:", path)
print("STATE: MISSION_LOCKED")
