from pathlib import Path
import json

LEGACY = Path(".ima/legacy/ori_legacy.json")

def load_legacy():
    if LEGACY.exists():
        try:
            return json.loads(LEGACY.read_text(encoding="utf-8"))
        except:
            pass
    return {}

def build_context(message=""):
    data = load_legacy()

    return {
        "identity": data.get("identity_pattern", {}),
        "vision": data.get("architectural_vision", {}),
        "laws": data.get("personal_laws", []),
        "legacy": data.get("legacy_summary_hebrew", ""),
        "message": message
    }
