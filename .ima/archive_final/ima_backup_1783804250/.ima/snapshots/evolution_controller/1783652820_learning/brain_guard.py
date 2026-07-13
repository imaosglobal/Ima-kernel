from pathlib import Path
import json
import time

ROOT = Path("learning")
CANONICAL = ROOT / "meta_orchestrator.py"

REGISTRY = Path(".ima/governance/brain_registry.json")


def create_registry():
    data = {
        "system": "IMA",
        "state": "LOCKED",
        "brain": str(CANONICAL),
        "orchestrator": str(CANONICAL),
        "policy": [
            "single_brain_only",
            "single_orchestrator_only",
            "block_duplicate_creation",
            "redirect_to_canonical_path"
        ],
        "locked_at": time.time()
    }

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)

    REGISTRY.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def verify_brain(path):
    p = Path(path)

    if "orchestrator" in p.name.lower() and p != CANONICAL:
        raise RuntimeError(
            f"IMA BLOCKED: duplicate orchestrator.\n"
            f"USE ONLY: {CANONICAL}"
        )

    return True


if __name__ == "__main__":
    create_registry()
    print("IMA SINGLE BRAIN LOCKED")
    print("PATH:", CANONICAL)
