#!/usr/bin/env python3
"""
IMA SELF EVOLUTION

Canonical system-awareness and integrity engine.

This component:
- reads the canonical authority
- reads the canonical manifest
- reads the canonical registry
- verifies component existence
- verifies SHA256 integrity
- creates system-awareness snapshots
- appends chronological logs
- updates its own canonical identity

It does not create a new Runtime.
It does not create an Orchestrator.
It does not autonomously modify arbitrary source code.
Integrity failures are reported explicitly for controlled repair.
"""

from pathlib import Path
import json
import hashlib
import time


ROOT = Path(__file__).resolve().parents[2]
SELF_DIR = ROOT / "evolution/SELF_EVOLUTION"

SELF = SELF_DIR / "IMA_SELF_EVOLUTION.py"
IDENTITY = SELF_DIR / "CANONICAL_IDENTITY.json"
MARKER = SELF_DIR / ".CANONICAL"

MANIFEST = ROOT / "CANONICAL_AUTHORITY_MANIFEST.json"
REGISTRY = ROOT / "governance/CANONICAL_REGISTRY.json"

SNAPSHOTS = SELF_DIR / "snapshots"
LOGS = SELF_DIR / "logs"


def sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def inspect_component(
    source: str,
    path: Path,
    expected_hash: str | None = None,
    key: str | None = None
) -> dict:

    exists = path.is_file()
    actual_hash = sha256(path) if exists else None

    return {
        "source": source,
        "key": key,
        "path": str(path),
        "exists": exists,
        "sha256": actual_hash,
        "expected_sha256": expected_hash,
        "hash_match": (
            exists
            and expected_hash is not None
            and actual_hash == expected_hash
        )
    }


def inspect_system() -> dict:

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    registry = json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )

    components = []

    # --------------------------------------------------------
    # MANIFEST COMPONENTS
    # --------------------------------------------------------

    for key, item in manifest.get("files", {}).items():

        path = Path(item["canonical_path"])

        components.append(
            inspect_component(
                source="manifest",
                key=key,
                path=path,
                expected_hash=item.get("sha256")
            )
        )

    # --------------------------------------------------------
    # REGISTRY COMPONENTS
    # --------------------------------------------------------

    for item in registry.get("allowed_components", []):

        path = Path(item["file"])

        components.append(
            inspect_component(
                source="registry",
                path=path,
                expected_hash=item.get("sha256")
            )
        )

    self_hash = sha256(SELF)

    summary = {
        "total_components_seen": len(components),
        "existing": sum(
            1 for x in components
            if x["exists"]
        ),
        "missing": sum(
            1 for x in components
            if not x["exists"]
        ),
        "hash_matches": sum(
            1 for x in components
            if x["hash_match"]
        ),
        "hash_mismatches": sum(
            1 for x in components
            if x["exists"] and not x["hash_match"]
        )
    }

    return {
        "component": "IMA_SELF_EVOLUTION",
        "type": "SYSTEM_AWARENESS_SNAPSHOT",
        "timestamp": time.time(),

        "authority": str(ROOT.resolve()),

        "self": {
            "path": str(SELF.resolve()),
            "exists": SELF.is_file(),
            "sha256": self_hash,
            "canonical": True
        },

        "components": components,
        "summary": summary
    }


def write_snapshot(snapshot: dict) -> tuple[Path, Path]:

    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time())

    snapshot_path = (
        SNAPSHOTS /
        f"system_awareness_{timestamp}.json"
    )

    log_path = (
        LOGS /
        "self_evolution_chronological.jsonl"
    )

    snapshot_path.write_text(
        json.dumps(
            snapshot,
            ensure_ascii=False,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    with log_path.open("a", encoding="utf-8") as f:

        f.write(
            json.dumps(
                snapshot,
                ensure_ascii=False
            ) + "\n"
        )

    return snapshot_path, log_path


def update_identity() -> str:

    digest = sha256(SELF)

    identity = {
        "canonical": True,
        "component": "SELF_EVOLUTION",
        "entry_file": "IMA_SELF_EVOLUTION.py",
        "runtime": "existing_runtime",
        "authority": ".ima/CANONICAL_AUTHORITY",
        "canonical_path": str(SELF),
        "marker": ".CANONICAL",
        "sha256": digest,
        "updated_at": time.time(),
        "status": "canonical_integrity_engine_active"
    }

    IDENTITY.write_text(
        json.dumps(
            identity,
            ensure_ascii=False,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    return digest


def synchronize_manifest() -> str:

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    digest = sha256(SELF)

    entry = manifest.setdefault(
        "files",
        {}
    ).setdefault(
        "evolution/SELF_EVOLUTION/IMA_SELF_EVOLUTION.py",
        {}
    )

    entry["canonical_path"] = str(SELF)
    entry["sha256"] = digest
    entry["size"] = SELF.stat().st_size

    MANIFEST.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    return digest


def main() -> int:

    if not SELF.is_file():
        print("[FAIL] SELF_EVOLUTION missing")
        return 1

    if not MARKER.is_file():
        print("[FAIL] Canonical marker missing")
        return 1

    if not MANIFEST.is_file():
        print("[FAIL] Manifest missing")
        return 1

    if not REGISTRY.is_file():
        print("[FAIL] Registry missing")
        return 1

    snapshot = inspect_system()

    snapshot_path, log_path = write_snapshot(snapshot)

    digest = update_identity()

    synchronize_manifest()

    print("=" * 80)
    print("IMA SELF EVOLUTION — CANONICAL INTEGRITY ENGINE")
    print("=" * 80)

    print(json.dumps(
        snapshot["summary"],
        ensure_ascii=False,
        indent=2
    ))

    print()
    print("[OK] Canonical authority inspected")
    print("[OK] Manifest inspected")
    print("[OK] Registry inspected")
    print("[OK] Components inspected")
    print("[OK] SHA256 verification performed")
    print("[OK] System-awareness snapshot written")
    print("[OK] Chronological log appended")
    print("[OK] Canonical identity updated")
    print("[OK] Manifest synchronized")
    print()
    print("SELF SHA256:")
    print(digest)
    print()
    print("SNAPSHOT:")
    print(snapshot_path)
    print()
    print("LOG:")
    print(log_path)
    print("=" * 80)

    if snapshot["summary"]["missing"] != 0:
        print("[FAIL] Missing components detected")
        return 2

    if snapshot["summary"]["hash_mismatches"] != 0:
        print("[FAIL] Hash mismatches detected")
        return 3

    print("STATUS: CANONICAL INTEGRITY VERIFIED")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
