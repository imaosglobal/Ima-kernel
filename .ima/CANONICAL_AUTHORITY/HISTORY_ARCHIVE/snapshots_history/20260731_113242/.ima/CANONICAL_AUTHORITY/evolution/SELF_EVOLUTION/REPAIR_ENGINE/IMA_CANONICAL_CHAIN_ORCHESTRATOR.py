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
