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
