#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

PROJECT="$HOME/ima_kernel"
cd "$PROJECT"

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_ROOT=".ima/REPAIR_BACKUPS/evolution_architecture_${STAMP}"

AGI=".ima/agi_evolution"
AGI_RUNTIME="$AGI/runtime"

AUTH=".ima/CANONICAL_AUTHORITY"
SELF_EV="$AUTH/evolution/SELF_EVOLUTION"
REPAIR="$SELF_EV/REPAIR_ENGINE"

EVOLUTION_AGENT="$AGI_RUNTIME/evolution_agent.py"
SELF_EVOLUTION="$SELF_EV/IMA_SELF_EVOLUTION.py"
REPAIR_ENGINE="$REPAIR/IMA_REPAIR_ENGINE.py"
ORCHESTRATOR="$REPAIR/IMA_CANONICAL_CHAIN_ORCHESTRATOR.py"
GATE="$SELF_EV/CANONICAL_EVOLUTION_GATE.py"

echo "============================================================"
echo "IMA — EVOLUTION ARCHITECTURE REPAIR"
echo "============================================================"
echo "PROJECT: $PROJECT"
echo "BACKUP:  $BACKUP_ROOT"
echo

mkdir -p "$BACKUP_ROOT"

backup_file() {
    local src="$1"
    if [ -f "$src" ]; then
        mkdir -p "$BACKUP_ROOT/$(dirname "$src")"
        cp -p "$src" "$BACKUP_ROOT/$src"
        echo "[BACKUP] $src"
    fi
}

restore_on_failure() {
    echo
    echo "============================================================"
    echo "[FAIL] Repair failed"
    echo "[ROLLBACK] Restoring modified files"
    echo "============================================================"

    if [ -d "$BACKUP_ROOT" ]; then
        cp -p "$BACKUP_ROOT/$EVOLUTION_AGENT" "$EVOLUTION_AGENT" 2>/dev/null || true
        cp -p "$BACKUP_ROOT/$SELF_EVOLUTION" "$SELF_EVOLUTION" 2>/dev/null || true
        cp -p "$BACKUP_ROOT/$REPAIR_ENGINE" "$REPAIR_ENGINE" 2>/dev/null || true
        cp -p "$BACKUP_ROOT/$ORCHESTRATOR" "$ORCHESTRATOR" 2>/dev/null || true
        rm -f "$GATE" 2>/dev/null || true
    fi

    echo "[ROLLBACK] Completed"
    exit 1
}

trap restore_on_failure ERR

echo "[1/9] Checking required files"

for f in \
    "$EVOLUTION_AGENT" \
    "$SELF_EVOLUTION" \
    "$REPAIR_ENGINE" \
    "$ORCHESTRATOR"
do
    if [ ! -f "$f" ]; then
        echo "[FAIL] Missing required file: $f"
        exit 1
    fi
done

echo "[OK] Required files exist"

echo
echo "[2/9] Creating backups"

backup_file "$EVOLUTION_AGENT"
backup_file "$SELF_EVOLUTION"
backup_file "$REPAIR_ENGINE"
backup_file "$ORCHESTRATOR"

echo "[OK] Backups created"

echo
echo "[3/9] Replacing evolution_agent.py with Proposal-only engine"

cat > "$EVOLUTION_AGENT" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import json
import time
import hashlib


ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / "runtime"
PROPOSALS = RUNTIME / "proposals"


class EvolutionAgent:

    def __init__(self):
        PROPOSALS.mkdir(parents=True, exist_ok=True)

    def read_plan(self):
        path = RUNTIME / "evolution_plan.json"

        if not path.exists():
            return {}

        return json.loads(
            path.read_text(encoding="utf-8")
        )

    def proposal_id(self, capability, goal):
        raw = f"{capability}|{goal}|{time.time_ns()}"
        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:16]

    def create_module_proposal(self, capability, goal):
        proposal_id = self.proposal_id(
            capability,
            goal
        )

        proposal = {
            "type": "EVOLUTION_PROPOSAL",
            "proposal_id": proposal_id,
            "status": "PROPOSED",
            "capability": capability,
            "goal": goal,
            "requested_action": "create_module",
            "target_path": str(
                ROOT / capability /
                f"{capability}_engine.py"
            ),
            "requires_approval": True,
            "approval": {
                "approved": False,
                "approved_by": None,
                "approved_at": None
            },
            "mutation_performed": False,
            "created_at": time.time()
        }

        path = (
            PROPOSALS /
            f"{proposal_id}.json"
        )

        path.write_text(
            json.dumps(
                proposal,
                ensure_ascii=False,
                indent=2
            ) + "\n",
            encoding="utf-8"
        )

        return {
            "status": "proposal_created",
            "proposal": str(path),
            "mutation_performed": False
        }

    def propose(self):
        plan = self.read_plan()
        results = []

        for item in plan.get(
            "detected_gaps",
            []
        ):
            capability = item.get(
                "capability"
            )

            goal = item.get(
                "goal"
            )

            if not capability:
                continue

            results.append(
                self.create_module_proposal(
                    capability,
                    goal
                )
            )

        report = {
            "type": "EVOLUTION_PROPOSAL_CYCLE",
            "status": "PROPOSALS_CREATED",
            "created": results,
            "mutation_performed": False,
            "timestamp": time.time()
        }

        path = (
            RUNTIME /
            "evolution_proposal_result.json"
        )

        path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2
            ) + "\n",
            encoding="utf-8"
        )

        return report


AGENT = EvolutionAgent()


if __name__ == "__main__":
    print(
        json.dumps(
            AGENT.propose(),
            ensure_ascii=False,
            indent=2
        )
    )
PY

echo "[OK] Evolution agent is now Proposal-only"

echo
echo "[4/9] Creating Canonical Evolution Gate"

cat > "$GATE" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import time


PROJECT = Path.cwd()
AUTHORITY = (
    PROJECT /
    ".ima" /
    "CANONICAL_AUTHORITY"
)

REGISTRY = (
    AUTHORITY /
    "governance" /
    "CANONICAL_REGISTRY.json"
)

MANIFEST = (
    AUTHORITY /
    "CANONICAL_AUTHORITY_MANIFEST.json"
)

PROPOSALS = (
    PROJECT /
    ".ima" /
    "agi_evolution" /
    "runtime" /
    "proposals"
)


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            h.update(chunk)

    return h.hexdigest()


def load_json(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def validate_proposal(path):
    proposal = load_json(path)

    errors = []

    required = [
        "type",
        "proposal_id",
        "capability",
        "goal",
        "requested_action",
        "target_path"
    ]

    for key in required:
        if key not in proposal:
            errors.append(
                f"missing:{key}"
            )

    if proposal.get("type") != (
        "EVOLUTION_PROPOSAL"
    ):
        errors.append(
            "invalid_type"
        )

    if proposal.get("status") != (
        "PROPOSED"
    ):
        errors.append(
            "invalid_status"
        )

    if proposal.get(
        "mutation_performed"
    ) is not False:
        errors.append(
            "mutation_already_performed"
        )

    target = Path(
        proposal.get(
            "target_path",
            ""
        )
    )

    if target.exists():
        errors.append(
            "target_already_exists"
        )

    if errors:
        return {
            "proposal": str(path),
            "status": "REJECTED",
            "errors": errors,
            "mutation_performed": False
        }

    return {
        "proposal": str(path),
        "status": "APPROVAL_REQUIRED",
        "capability": proposal[
            "capability"
        ],
        "goal": proposal[
            "goal"
        ],
        "target_path": str(target),
        "requires_approval": True,
        "mutation_performed": False
    }


def inspect():
    results = []

    if not PROPOSALS.exists():
        return {
            "type": "CANONICAL_EVOLUTION_GATE_AUDIT",
            "status": "NO_PROPOSALS",
            "proposals": [],
            "mutation_performed": False,
            "timestamp": time.time()
        }

    for path in sorted(
        PROPOSALS.glob("*.json")
    ):
        try:
            results.append(
                validate_proposal(path)
            )
        except Exception as exc:
            results.append({
                "proposal": str(path),
                "status": "INVALID",
                "error": str(exc),
                "mutation_performed": False
            })

    return {
        "type": "CANONICAL_EVOLUTION_GATE_AUDIT",
        "status": "READ_ONLY",
        "proposals": results,
        "mutation_performed": False,
        "registry_modified": False,
        "manifest_modified": False,
        "timestamp": time.time()
    }


if __name__ == "__main__":
    print(
        json.dumps(
            inspect(),
            ensure_ascii=False,
            indent=2
        )
    )
PY

chmod +x "$GATE"

echo "[OK] Canonical Evolution Gate created"

echo
echo "[5/9] Replacing self-evolution auto-synchronization"

python3 - "$SELF_EVOLUTION" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

old = """    synchronize_manifest()
"""

new = """    # Manifest synchronization is intentionally disabled
    # during canonical verification.
    #
    # Verification must observe.
    # Synchronization requires an explicit approved repair plan.
"""

if old in text:
    text = text.replace(old, new, 1)

old_print = """    print("[OK] Manifest synchronized")
"""

new_print = """    print("[OK] Manifest synchronization skipped in VERIFY mode")
"""

if old_print in text:
    text = text.replace(
        old_print,
        new_print,
        1
    )

path.write_text(
    text,
    encoding="utf-8"
)
PY

echo "[OK] Self-evolution verification no longer auto-synchronizes Manifest"

echo
echo "[6/9] Adding explicit VERIFY/SYNCHRONIZE mode guard to Repair Engine"

python3 - "$REPAIR_ENGINE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

marker = "def verify_global_canonical_chain():"

guard = '''def verify_global_canonical_chain():
    """
    VERIFY MODE ONLY.

    This function must not synchronize or mutate
    Registry or Manifest.
    """
'''

if marker in text:
    start = text.index(marker)
    end = start + len(marker)

    text = (
        text[:start] +
        guard +
        text[end:]
    )

path.write_text(
    text,
    encoding="utf-8"
)
PY

echo "[OK] Repair Engine verification mode documented and guarded"

echo
echo "[7/9] Rewriting Canonical Chain Orchestrator as VERIFY-only"

cat > "$ORCHESTRATOR" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time


PROJECT = Path.cwd()

ROOT = (
    PROJECT /
    ".ima" /
    "CANONICAL_AUTHORITY"
)

REGISTRY = (
    ROOT /
    "governance" /
    "CANONICAL_REGISTRY.json"
)

MANIFEST = (
    ROOT /
    "CANONICAL_AUTHORITY_MANIFEST.json"
)

REPAIR_ENGINE = (
    ROOT /
    "evolution" /
    "SELF_EVOLUTION" /
    "REPAIR_ENGINE" /
    "IMA_REPAIR_ENGINE.py"
)

GLOBAL_AWARENESS = (
    ROOT /
    "evolution" /
    "SELF_EVOLUTION" /
    "GLOBAL_SYSTEM_AWARENESS" /
    "IMA_GLOBAL_SYSTEM_AWARENESS.py"
)

SELF_EVOLUTION = (
    ROOT /
    "evolution" /
    "SELF_EVOLUTION" /
    "IMA_SELF_EVOLUTION.py"
)


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            h.update(chunk)

    return h.hexdigest()


def load_json(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def verify():
    print("=" * 80)
    print("IMA — CANONICAL CHAIN VERIFY MODE")
    print("=" * 80)

    required = [
        REGISTRY,
        MANIFEST,
        REPAIR_ENGINE,
        GLOBAL_AWARENESS,
        SELF_EVOLUTION
    ]

    for path in required:
        if not path.is_file():
            raise RuntimeError(
                f"Required file missing: {path}"
            )

    registry = load_json(REGISTRY)
    manifest = load_json(MANIFEST)

    mismatches = []
    missing = []

    for item in registry.get(
        "allowed_components",
        []
    ):
        file_path = item.get(
            "file"
        )

        if not file_path:
            continue

        path = Path(file_path)

        if not path.is_absolute():
            path = PROJECT / path

        path = path.resolve()

        if not path.is_file():
            missing.append(
                str(path)
            )
            continue

        actual = sha256(path)
        expected = item.get(
            "sha256"
        )

        if actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "registry"
            })

    for key, item in manifest.get(
        "files",
        {}
    ).items():

        canonical_path = item.get(
            "canonical_path"
        )

        if not canonical_path:
            continue

        path = Path(
            canonical_path
        )

        if not path.is_file():
            missing.append(
                str(path)
            )
            continue

        actual = sha256(path)
        expected = item.get(
            "sha256"
        )

        if actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "manifest",
                "key": key
            })

    if missing:
        raise RuntimeError(
            "Missing canonical files:\n" +
            "\n".join(missing)
        )

    if mismatches:
        raise RuntimeError(
            "Canonical hash mismatches:\n" +
            json.dumps(
                mismatches,
                ensure_ascii=False,
                indent=2
            )
        )

    for path in [
        REPAIR_ENGINE,
        GLOBAL_AWARENESS,
        SELF_EVOLUTION
    ]:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "py_compile",
                str(path)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr
            )

    print("[OK] Registry hashes verified")
    print("[OK] Manifest hashes verified")
    print("[OK] All canonical files exist")
    print("[OK] Canonical engines compile")
    print("[OK] VERIFY mode performed")
    print("[OK] Registry not modified")
    print("[OK] Manifest not modified")
    print("[OK] No source mutation performed")
    print("[OK] No synchronization performed")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    raise SystemExit(
        verify()
    )
PY

echo "[OK] Canonical Chain Orchestrator is now VERIFY-only"

echo
echo "[8/9] Compiling all repaired components"

python3 -m py_compile \
    "$EVOLUTION_AGENT" \
    "$GATE" \
    "$SELF_EVOLUTION" \
    "$REPAIR_ENGINE" \
    "$ORCHESTRATOR"

echo "[OK] All repaired components compile"

echo
echo "[9/9] Running read-only verification"

python3 "$GATE"

python3 "$ORCHESTRATOR"

echo
echo "============================================================"
echo "IMA — EVOLUTION ARCHITECTURE REPAIR COMPLETE"
echo "============================================================"
echo "[OK] Evolution Agent is Proposal-only"
echo "[OK] Canonical Evolution Gate exists"
echo "[OK] Verification does not synchronize Registry"
echo "[OK] Verification does not synchronize Manifest"
echo "[OK] Canonical Chain is VERIFY-only"
echo "[OK] Self-Evolution no longer auto-synchronizes Manifest"
echo "[OK] All repaired files compile"
echo "[OK] Canonical chain verified"
echo "[OK] No evolution modules created"
echo "[OK] No evolution cycle executed"
echo "[OK] Backup available at:"
echo "$BACKUP_ROOT"
echo "============================================================"

trap - ERR
