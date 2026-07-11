#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

mkdir -p .ima/governance

cat > .ima/governance/architecture_guard.py <<'PY'
from pathlib import Path
import json
import time

ROOT = Path(".")
REGISTRY = Path(".ima/governance/IMA_PRODUCT_ARCHITECTURE_LOCK.json")

CANONICAL_BRAIN = Path("learning/meta_orchestrator.py")
CANONICAL_BODY = Path("kernel/runtime/ENTRYPOINT.js")


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
PY


python3 -m py_compile .ima/governance/architecture_guard.py

python3 .ima/governance/architecture_guard.py

git add .ima/governance/architecture_guard.py

git commit -m "IMA architecture guard locked canonical brain and body"

git tag -a IMA_KERNEL_ARCHITECTURE_GUARD_LOCKED_v1 \
-m "Architecture guard locked canonical paths"

echo "=== ARCHITECTURE GUARD LOCKED ==="
echo "BRAIN: learning/meta_orchestrator.py"
echo "BODY: kernel/runtime/ENTRYPOINT.js"
echo "TAG: IMA_KERNEL_ARCHITECTURE_GUARD_LOCKED_v1"
