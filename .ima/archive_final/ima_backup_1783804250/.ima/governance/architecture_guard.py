from pathlib import Path
import json
import time

ROOT = Path(".")
REGISTRY = Path(".ima/governance/IMA_PRODUCT_ARCHITECTURE_LOCK.json")

CANONICAL_BRAIN = Path("learning/meta_orchestrator.py")
CANONICAL_BODY = Path("IMA_START.py")


class ArchitectureViolation(Exception):
    pass


def load_policy():
    if not REGISTRY.exists():
        raise ArchitectureViolation(
            "IMA architecture registry missing"
        )

    return json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )


def check_brain(path):
    p = Path(path)

    if "orchestrator" in p.name.lower():
        if p != CANONICAL_BRAIN:
            raise ArchitectureViolation(
                f"IMA BLOCKED duplicate brain/orchestrator\n"
                f"USE ONLY: {CANONICAL_BRAIN}"
            )

    return True


def check_body(path):
    p = Path(path)

    if "entrypoint" in p.name.lower():
        if p != CANONICAL_BODY:
            raise ArchitectureViolation(
                f"IMA BLOCKED duplicate runtime body\n"
                f"USE ONLY: {CANONICAL_BODY}"
            )

    return True


def verify_architecture(path):
    check_brain(path)
    check_body(path)
    return True


def guard_status():
    policy = load_policy()

    return {
        "system": "IMA",
        "guard": "architecture_guard",
        "state": "ACTIVE",
        "brain": str(CANONICAL_BRAIN),
        "body": str(CANONICAL_BODY),
        "policy": policy.get("rules", []),
        "checked_at": time.time()
    }


if __name__ == "__main__":
    print(
        json.dumps(
            guard_status(),
            ensure_ascii=False,
            indent=2
        )
    )
