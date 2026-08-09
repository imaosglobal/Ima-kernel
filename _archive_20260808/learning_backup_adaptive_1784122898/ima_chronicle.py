from pathlib import Path
import json
import time

ROOT = Path(".")
CHRONICLE = ROOT / ".ima/governance/ima_chronicle.json"

CANONICAL = {
    "brain": "learning/meta_orchestrator.py",
    "orchestrator": "learning/meta_orchestrator.py",
    "runtime": "kernel/runtime/SYSTEM_KERNEL_UNIFIED_RUNTIME_V1.js",
    "registry": ".ima/governance/brain_registry.json"
}

POLICY = {
    "state": "LOCKED",
    "single_brain": True,
    "single_orchestrator": True,
    "block_duplicate_creation": True,
    "redirect_unknown_paths": True
}

def create_chronicle():
    CHRONICLE.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "system": "IMA",
        "type": "canonical_chronicle",
        "locked_at": time.time(),
        "canonical": CANONICAL,
        "policy": POLICY
    }

    CHRONICLE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("IMA CHRONICLE LOCKED")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def verify_path(path):
    p = str(path).lower()

    forbidden = [
        "new_brain",
        "new_orchestrator",
        "meta_orchestrator_v2",
        "brain2",
        "orchestrator2"
    ]

    for item in forbidden:
        if item in p:
            raise RuntimeError(
                "IMA BLOCKED DUPLICATE CREATION\n"
                "USE:\n"
                "learning/meta_orchestrator.py"
            )

    return True


if __name__ == "__main__":
    create_chronicle()
