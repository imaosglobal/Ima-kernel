import json
from pathlib import Path

REGISTRY = Path("product/identity/founder_registry.json")

def load_founder_identity():
    if not REGISTRY.exists():
        return {
            "founder": None,
            "linked": False
        }

    data = json.loads(
        REGISTRY.read_text(encoding="utf8")
    )

    return {
        "founder": data.get("founder"),
        "linked": True,
        "source": data.get("founder", {}).get("legacy_source")
    }
