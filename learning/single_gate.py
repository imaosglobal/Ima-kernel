from pathlib import Path
import hashlib
import json
import time


GATE_TARGET = Path("learning/evolution_controller.py")
REGISTRY = Path(".ima/governance/single_gate.json")
ALERTS = Path(".ima/governance/gate_alerts.jsonl")


def hash_file(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def create_or_update_gate():

    REGISTRY.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "name": "IMA_SINGLE_ENTRY_GATE",
        "target": str(GATE_TARGET),
        "hash": hash_file(GATE_TARGET),
        "version": 1,
        "status": "protected",
        "rules": [
            "snapshot_before_change",
            "compile_check_required",
            "health_check_required",
            "hash_verification_required"
        ],
        "created": time.time()
    }

    REGISTRY.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("SINGLE GATE CREATED")
    print(data["hash"])


def verify_gate():

    data=json.loads(
        REGISTRY.read_text(
            encoding="utf-8"
        )
    )

    current=hash_file(
        GATE_TARGET
    )

    if current != data["hash"]:

        ALERTS.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with ALERTS.open(
            "a",
            encoding="utf-8"
        ) as f:
            f.write(
                json.dumps({
                    "time":time.time(),
                    "event":"GATE_MODIFIED"
                })+"\n"
            )

        raise RuntimeError(
            "IMA SINGLE ENTRY GATE BLOCKED"
        )

    return True


if __name__=="__main__":
    print("STATUS:",verify_gate())
