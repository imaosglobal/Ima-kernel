from pathlib import Path
import json

CANONICAL_BRAIN = Path("learning/meta_orchestrator.py")
CANONICAL_ORCHESTRATOR = Path("learning/meta_orchestrator.py")

CONNECTORS = [
    Path("learning/module_registry.py")
]

REGISTRY = Path(".ima/governance/brain_registry.json")


def create_registry():

    data = {
        "system": "IMA",
        "state": "LOCKED",
        "brain": str(CANONICAL_BRAIN),
        "orchestrator": str(CANONICAL_ORCHESTRATOR),
        "connectors": [str(x) for x in CONNECTORS],
        "policy": [
            "single_brain_only",
            "single_orchestrator_only",
            "connectors_allowed",
            "block_duplicate_creation"
        ]
    }

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)

    REGISTRY.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def verify_brain(path):

    p = Path(path)

    if p == CANONICAL_BRAIN:
        return True

    if p in CONNECTORS:
        return True

    if "orchestrator" in p.name.lower():
        raise RuntimeError(
            "IMA BLOCKED duplicate orchestrator. USE: learning/meta_orchestrator.py"
        )

    return True


if __name__ == "__main__":
    create_registry()
    print("IMA CANONICAL BRAIN LOCKED")
    print(CANONICAL_BRAIN)
