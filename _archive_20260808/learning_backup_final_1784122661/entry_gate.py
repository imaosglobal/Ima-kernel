from pathlib import Path
import hashlib
import json


GATE = Path(".ima/governance/entry_gate.json")
HASHES = Path(".ima/governance/checksums.json")


def verify_entry_gate():

    if not GATE.exists():
        raise RuntimeError("ENTRY GATE MISSING")

    if not HASHES.exists():
        raise RuntimeError("HASH REGISTRY MISSING")


    data=json.loads(
        HASHES.read_text(encoding="utf-8")
    )

    target=Path(
        "learning/evolution_controller.py"
    )

    current=hashlib.sha256(
        target.read_bytes()
    ).hexdigest()


    saved=data.get(
        "evolution_controller.py"
    )


    if current != saved:
        raise RuntimeError(
            "ENTRY GATE BLOCKED: unauthorized change"
        )


    return True


if __name__=="__main__":
