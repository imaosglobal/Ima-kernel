from pathlib import Path
import hashlib
import json
import time


GATE_FILE = Path("learning/evolution_controller.py")
REGISTRY = Path(".ima/governance/entry_gate_registry.json")
ALERT = Path(".ima/governance/gate_alerts.jsonl")


def sha256(file):
    return hashlib.sha256(
        file.read_bytes()
    ).hexdigest()


def load_registry():
    return json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )


def alert(message):
    ALERT.parent.mkdir(parents=True, exist_ok=True)

    with ALERT.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps({
                "time": time.time(),
                "alert": message
            }, ensure_ascii=False)
            + "\n"
        )


def verify_gate():

    registry = load_registry()

    current = sha256(GATE_FILE)
    saved = registry["hash"]

    if current != saved:
        alert(
            "ENTRY GATE MODIFIED: " + str(GATE_FILE)
        )

        raise RuntimeError(
            "BLOCKED: SINGLE ENTRY GATE WAS CHANGED"
        )

    return True


if __name__ == "__main__":
    print("GATE STATUS:", verify_gate())
