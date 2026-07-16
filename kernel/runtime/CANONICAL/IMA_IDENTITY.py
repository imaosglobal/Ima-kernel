from pathlib import Path
import json
import time

ROOT = Path.cwd()

def load_identity():
    identity_file = ROOT / "IMA_IDENTITY.md"
    link_file = ROOT / ".ima/governance/IMA_IDENTITY_LINK.json"
    mission_file = ROOT / ".ima/governance/mission_registry.json"

    result = {
        "system": "IMA",
        "status": "IDENTITY_UNAVAILABLE",
        "time": int(time.time()),
        "document": None,
        "links": {},
        "mission": {}
    }

    if identity_file.exists():
        result["document"] = identity_file.read_text()

    if link_file.exists():
        result["links"] = json.loads(link_file.read_text())

    if mission_file.exists():
        result["mission"] = json.loads(mission_file.read_text())

    result["status"] = "IDENTITY_CANONICAL"
    return result


if __name__ == "__main__":
    print(json.dumps(load_identity(), indent=2, ensure_ascii=False))
