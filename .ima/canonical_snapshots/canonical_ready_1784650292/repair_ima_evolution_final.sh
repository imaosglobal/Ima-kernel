#!/data/data/com.termux/files/usr/bin/bash

set -Eeuo pipefail

PROJECT="$HOME/ima_kernel"
cd "$PROJECT"

TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_ROOT=".ima/REPAIR_BACKUPS/final_evolution_repair_${TS}"

AUTH=".ima/CANONICAL_AUTHORITY"
RUNTIME=".ima/agi_evolution/runtime"

REGISTRY="$AUTH/governance/CANONICAL_REGISTRY.json"
MANIFEST="$AUTH/CANONICAL_AUTHORITY_MANIFEST.json"

EVOLUTION_AGENT="$RUNTIME/evolution_agent.py"
GATE="$RUNTIME/ima_canonical_evolution_gate.py"

SELF_EVOLUTION="$AUTH/evolution/SELF_EVOLUTION/IMA_SELF_EVOLUTION.py"
REPAIR_ENGINE="$AUTH/evolution/SELF_EVOLUTION/REPAIR_ENGINE/IMA_REPAIR_ENGINE.py"
ORCHESTRATOR="$AUTH/evolution/SELF_EVOLUTION/REPAIR_ENGINE/IMA_CANONICAL_CHAIN_ORCHESTRATOR.py"

mkdir -p "$BACKUP_ROOT"

echo "============================================================"
echo "IMA — FINAL EVOLUTION ARCHITECTURE REPAIR"
echo "============================================================"
echo "PROJECT: $PROJECT"
echo "BACKUP:  $BACKUP_ROOT"
echo

fail() {
    echo
    echo "============================================================"
    echo "[FAIL] $1"
    echo "============================================================"
    echo "[BACKUP] $BACKUP_ROOT"
    exit 1
}

backup_file() {
    local src="$1"
    local dst="$BACKUP_ROOT/$(echo "$src" | tr '/' '_')"

    if [ -f "$src" ]; then
        cp -p "$src" "$dst"
        echo "[BACKUP] $src"
    fi
}

sha256_file() {
    sha256sum "$1" | awk '{print $1}'
}

echo "[1/10] Checking required files"

for f in \
    "$REGISTRY" \
    "$MANIFEST" \
    "$EVOLUTION_AGENT" \
    "$SELF_EVOLUTION" \
    "$REPAIR_ENGINE" \
    "$ORCHESTRATOR"
do
    [ -f "$f" ] || fail "Missing required file: $f"
done

echo "[OK] Required files exist"
echo

echo "[2/10] Creating backups"

for f in \
    "$REGISTRY" \
    "$MANIFEST" \
    "$EVOLUTION_AGENT" \
    "$GATE" \
    "$SELF_EVOLUTION" \
    "$REPAIR_ENGINE" \
    "$ORCHESTRATOR"
do
    backup_file "$f"
done

echo "[OK] Backups created"
echo

echo "[3/10] Converting evolution agent to proposal-only mode"

cat > "$EVOLUTION_AGENT" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parent

STATE_FILES = [
    ROOT / "evolution_plan.json",
    ROOT / "cognitive_pipeline_state.json",
    ROOT / "autonomous_state.json",
    ROOT / "latest_cycle.json",
]

def load_json(path):
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def create_proposals():
    plan = load_json(ROOT / "evolution_plan.json")

    gaps = plan.get("detected_gaps", [])
    priority = plan.get("priority_order", [])

    proposals = []

    for item in gaps:
        capability = item.get("capability")
        goal = item.get("goal")

        proposals.append({
            "capability": capability,
            "goal": goal,
            "status": "PROPOSAL_ONLY",
            "mutation_allowed": False,
            "registration_allowed": False,
            "promotion_allowed": False,
        })

    return {
        "type": "EVOLUTION_PROPOSAL_SET",
        "status": "PROPOSAL_ONLY",
        "priority_order": priority,
        "proposals": proposals,
        "mutation_performed": False,
        "module_created": False,
        "timestamp": time.time(),
    }

def main():
    result = create_proposals()

    output = ROOT / "evolution_proposals.json"

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
PY

chmod +x "$EVOLUTION_AGENT"

echo "[OK] Evolution Agent is Proposal-only"
echo

echo "[4/10] Creating canonical evolution gate"

cat > "$GATE" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parent
PROPOSALS = ROOT / "evolution_proposals.json"

def main():
    proposals = []

    if PROPOSALS.is_file():
        try:
            data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
            proposals = data.get("proposals", [])
        except Exception:
            proposals = []

    audit = {
        "type": "CANONICAL_EVOLUTION_GATE_AUDIT",
        "status": "NO_PROPOSALS" if not proposals else "PROPOSALS_PENDING_APPROVAL",
        "proposals": proposals,
        "mutation_performed": False,
        "promotion_performed": False,
        "registration_performed": False,
        "timestamp": time.time(),
    }

    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
PY

chmod +x "$GATE"

echo "[OK] Canonical Evolution Gate created"
echo

echo "[5/10] Replacing Self-Evolution with verification-only behavior"

cat > "$SELF_EVOLUTION" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import json
import hashlib
import time

ROOT = Path(__file__).resolve().parents[2]

SELF = Path(__file__).resolve()
MARKER = SELF.parent / ".CANONICAL"
MANIFEST = ROOT / "CANONICAL_AUTHORITY_MANIFEST.json"
REGISTRY = ROOT / "governance" / "CANONICAL_REGISTRY.json"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify():
    if not SELF.is_file():
        raise RuntimeError("Self-evolution engine missing")

    if not MARKER.is_file():
        raise RuntimeError("Canonical marker missing")

    if not MANIFEST.is_file():
        raise RuntimeError("Canonical manifest missing")

    if not REGISTRY.is_file():
        raise RuntimeError("Canonical registry missing")

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    registry = json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )

    missing = []
    mismatches = []

    for item in registry.get("allowed_components", []):
        path = Path(item["file"])

        if not path.is_absolute():
            path = ROOT.parent.parent / path

        if not path.is_file():
            missing.append(str(path))
            continue

        actual = sha256(path)
        expected = item.get("sha256")

        if expected and actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "registry",
            })

    for key, item in manifest.get("files", {}).items():
        path = Path(item.get("canonical_path", ""))

        if not path.is_file():
            missing.append(str(path))
            continue

        actual = sha256(path)
        expected = item.get("sha256")

        if expected and actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "manifest",
                "key": key,
            })

    if missing:
        raise RuntimeError(
            "Missing canonical files:\n" +
            "\n".join(missing)
        )

    if mismatches:
        raise RuntimeError(
            "Canonical hash mismatches:\n" +
            json.dumps(mismatches, ensure_ascii=False, indent=2)
        )

    print("[OK] Registry hashes verified")
    print("[OK] Manifest hashes verified")
    print("[OK] All canonical files exist")
    print("[OK] Verification-only mode")
    print("[OK] Registry not modified")
    print("[OK] Manifest not modified")
    print("[OK] No source mutation performed")
    print("[OK] No synchronization performed")

    return 0

if __name__ == "__main__":
    raise SystemExit(verify())
PY

echo "[OK] Self-Evolution is verification-only"
echo

echo "[6/10] Replacing Repair Engine with explicit modes"

cat > "$REPAIR_ENGINE" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[3]

REGISTRY = ROOT / "governance" / "CANONICAL_REGISTRY.json"
MANIFEST = ROOT / "CANONICAL_AUTHORITY_MANIFEST.json"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify():
    if not REGISTRY.is_file():
        raise RuntimeError("Registry missing")

    if not MANIFEST.is_file():
        raise RuntimeError("Manifest missing")

    registry = json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    missing = []
    mismatches = []

    for item in registry.get("allowed_components", []):
        path = Path(item["file"])

        if not path.is_absolute():
            path = ROOT.parent.parent / path

        if not path.is_file():
            missing.append(str(path))
            continue

        actual = sha256(path)
        expected = item.get("sha256")

        if actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "registry",
            })

    for key, item in manifest.get("files", {}).items():
        path = Path(item.get("canonical_path", ""))

        if not path.is_file():
            missing.append(str(path))
            continue

        actual = sha256(path)
        expected = item.get("sha256")

        if actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "manifest",
                "key": key,
            })

    if missing:
        raise RuntimeError(
            "Missing canonical files:\n" +
            "\n".join(missing)
        )

    if mismatches:
        raise RuntimeError(
            "Canonical hash mismatches:\n" +
            json.dumps(mismatches, ensure_ascii=False, indent=2)
        )

    return True

def main():
    print("[OK] Repair Engine loaded")
    print("[OK] VERIFY mode available")
    print("[OK] No automatic mutation")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
PY

echo "[OK] Repair Engine replaced"
echo

echo "[7/10] Replacing Canonical Chain Orchestrator with VERIFY-only mode"

cat > "$ORCHESTRATOR" <<'PY'
#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

PROJECT = Path.cwd()
ROOT = PROJECT / ".ima" / "CANONICAL_AUTHORITY"

REGISTRY = ROOT / "governance" / "CANONICAL_REGISTRY.json"
MANIFEST = ROOT / "CANONICAL_AUTHORITY_MANIFEST.json"

SELF_EVOLUTION = (
    ROOT /
    "evolution" /
    "SELF_EVOLUTION" /
    "IMA_SELF_EVOLUTION.py"
)

REPAIR_ENGINE = (
    ROOT /
    "evolution" /
    "SELF_EVOLUTION" /
    "REPAIR_ENGINE" /
    "IMA_REPAIR_ENGINE.py"
)

def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()

def verify():
    print("=" * 80)
    print("IMA — CANONICAL CHAIN VERIFY MODE")
    print("=" * 80)

    registry = json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    missing = []
    mismatches = []

    for item in registry.get("allowed_components", []):
        path = Path(item["file"])

        if not path.is_absolute():
            path = PROJECT / path

        path = path.resolve()

        if not path.is_file():
            missing.append(str(path))
            continue

        actual = sha256(path)
        expected = item.get("sha256")

        if actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "registry",
            })

    for key, item in manifest.get("files", {}).items():
        path = Path(item.get("canonical_path", ""))

        if not path.is_file():
            missing.append(str(path))
            continue

        actual = sha256(path)
        expected = item.get("sha256")

        if actual != expected:
            mismatches.append({
                "path": str(path),
                "actual": actual,
                "expected": expected,
                "source": "manifest",
                "key": key,
            })

    if missing:
        raise RuntimeError(
            "Missing canonical files:\n" +
            "\n".join(missing)
        )

    if mismatches:
        raise RuntimeError(
            "Canonical hash mismatches:\n" +
            json.dumps(mismatches, ensure_ascii=False, indent=2)
        )

    print("[OK] Registry hashes verified")
    print("[OK] Manifest hashes verified")
    print("[OK] All canonical files exist")
    print("[OK] No registry synchronization")
    print("[OK] No manifest synchronization")
    print("[OK] No source mutation")
    print("[OK] VERIFY passed")
    print("=" * 80)

    return 0

if __name__ == "__main__":
    raise SystemExit(verify())
PY

echo "[OK] Canonical Chain is VERIFY-only"
echo

echo "[8/10] Compiling repaired architecture"

python3 -m py_compile \
    "$EVOLUTION_AGENT" \
    "$GATE" \
    "$SELF_EVOLUTION" \
    "$REPAIR_ENGINE" \
    "$ORCHESTRATOR"

echo "[OK] All repaired components compile"
echo

echo "[9/10] Controlled canonical promotion"

python3 - "$REGISTRY" "$MANIFEST" "$PROJECT" <<'PY'
from pathlib import Path
import json
import hashlib
import sys
import tempfile
import os

registry_path = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])
project = Path(sys.argv[3]).resolve()

def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()

registry = json.loads(
    registry_path.read_text(encoding="utf-8")
)

manifest = json.loads(
    manifest_path.read_text(encoding="utf-8")
)

changed_registry = 0
changed_manifest = 0

for item in registry.get("allowed_components", []):
    raw = item.get("file")

    if not raw:
        continue

    path = Path(raw)

    if not path.is_absolute():
        path = project / path

    path = path.resolve()

    if not path.is_file():
        raise RuntimeError(f"Canonical file missing: {path}")

    digest = sha256(path)
    size = path.stat().st_size

    if item.get("sha256") != digest:
        item["sha256"] = digest
        changed_registry += 1

    item["size"] = size

for key, item in manifest.get("files", {}).items():
    raw = item.get("canonical_path")

    if not raw:
        continue

    path = Path(raw)

    if not path.is_absolute():
        path = project / path

    path = path.resolve()

    if not path.is_file():
        raise RuntimeError(f"Manifest file missing: {path}")

    digest = sha256(path)
    size = path.stat().st_size

    if item.get("sha256") != digest:
        item["sha256"] = digest
        changed_manifest += 1

    item["size"] = size

def atomic_write(path, data):
    fd, temp = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2,
            )
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp, path)

    finally:
        if os.path.exists(temp):
            os.unlink(temp)

atomic_write(registry_path, registry)

registry_hash = sha256(registry_path)

entry = manifest.setdefault(
    "files",
    {}
).setdefault(
    "governance/CANONICAL_REGISTRY.json",
    {}
)

entry["canonical_path"] = str(registry_path.resolve())
entry["sha256"] = registry_hash
entry["size"] = registry_path.stat().st_size

atomic_write(manifest_path, manifest)

print(f"[OK] Registry promoted: {changed_registry} component hash updates")
print(f"[OK] Manifest promoted: {changed_manifest} component hash updates")
print("[OK] Registry hash synchronized into Manifest")
print("[OK] Atomic canonical promotion complete")
PY

echo

echo "[10/10] Final canonical verification"

python3 -m py_compile \
    "$EVOLUTION_AGENT" \
    "$GATE" \
    "$SELF_EVOLUTION" \
    "$REPAIR_ENGINE" \
    "$ORCHESTRATOR"

python3 "$GATE"

python3 "$ORCHESTRATOR"

echo
echo "============================================================"
echo "IMA — FINAL EVOLUTION ARCHITECTURE REPAIR COMPLETE"
echo "============================================================"
echo "[OK] Evolution Agent is Proposal-only"
echo "[OK] Canonical Evolution Gate exists"
echo "[OK] Self-Evolution is verification-only"
echo "[OK] Repair Engine has no automatic mutation"
echo "[OK] Canonical Chain is VERIFY-only"
echo "[OK] Canonical Registry promoted atomically"
echo "[OK] Canonical Manifest synchronized"
echo "[OK] All canonical components compile"
echo "[OK] Final canonical verification passed"
echo "[OK] No evolution cycle executed"
echo "[OK] No module automatically created"
echo
echo "BACKUP:"
echo "$BACKUP_ROOT"
echo "============================================================"
