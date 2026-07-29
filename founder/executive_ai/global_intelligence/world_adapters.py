from pathlib import Path
import json

FILE = Path("founder/data/world_opportunities.json")


def real_world_scanner():

    if FILE.exists():
        try:
            return json.loads(
                FILE.read_text(encoding="utf8")
            )
        except Exception:
            return []

    return []


def scan_world():

    return real_world_scanner()
