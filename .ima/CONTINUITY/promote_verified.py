#!/usr/bin/env python3
import os, json, hashlib, ast, shutil, time, subprocess
from pathlib import Path

ROOT = Path.cwd()
CONT = ROOT / ".ima" / "CONTINUITY"
ARCH = ROOT / ".ima" / "CANONICAL_AUTHORITY" / "HISTORY_ARCHIVE"
CURRENT = ROOT / ".ima" / "CANONICAL_AUTHORITY" / "SINGLE_SNAPSHOT" / "CURRENT"

REG = CONT / "candidate_registry.jsonl"
PROV = CONT / "provenance.jsonl"
PROMOTED = CONT / "promoted_registry.jsonl"
REPORT = CONT / "CONTINUITY_REPORT.md"

EXCLUDE = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "dist", "build"
}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def valid_file(p):
    try:
        if p.suffix == ".py":
            ast.parse(p.read_text(encoding="utf-8", errors="strict"))
        elif p.suffix == ".json":
            json.loads(p.read_text(encoding="utf-8"))
        return True, "validated"
    except Exception as e:
        return False, repr(e)

def walk(root):
    if not root.exists():
        return
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(x in EXCLUDE for x in p.parts):
            continue
        yield p

candidates = []
for p in walk(ARCH):
    if p.suffix not in {".py", ".json", ".md", ".jsonl"}:
        continue

    ok, reason = valid_file(p)
    item = {
        "source": str(p.relative_to(ROOT)),
        "sha256": sha256(p),
        "type": p.suffix[1:],
        "validated": ok,
        "reason": reason,
        "timestamp": time.time(),
        "promotion_policy": "verified_continuity_only"
    }
    candidates.append(item)

with open(REG, "w", encoding="utf-8") as f:
    for x in candidates:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")

# Promote only canonical continuity/documentation infrastructure.
# Historical executable code is NOT blindly activated.
promotable = []

for x in candidates:
    src = ROOT / x["source"]

    if not x["validated"]:
        continue

    rel = src.relative_to(ARCH)

    # Documentation / metadata / declarative knowledge may be promoted
    # into the continuity candidate area for future explicit review.
    if src.suffix in {".md", ".json", ".jsonl"}:
        dst = CONT / "candidates" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

        promotable.append({
            **x,
            "destination": str(dst.relative_to(ROOT)),
            "status": "candidate_promoted",
            "activation": "not_runtime_activated"
        })

with open(PROMOTED, "w", encoding="utf-8") as f:
    for x in promotable:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")

with open(PROV, "a", encoding="utf-8") as f:
    for x in promotable:
        f.write(json.dumps({
            "event": "continuity_candidate_promotion",
            "source": x["source"],
            "destination": x["destination"],
            "sha256": x["sha256"],
            "status": x["status"],
            "activation": x["activation"],
            "timestamp": time.time()
        }, ensure_ascii=False) + "\n")

# Snapshot of currently verified continuity state.
snapshot = CONT / "snapshots" / time.strftime("%Y%m%d_%H%M%S")
snapshot.mkdir(parents=True, exist_ok=True)

for name in [
    "candidate_registry.jsonl",
    "promoted_registry.jsonl",
    "provenance.jsonl"
]:
    src = CONT / name
    if src.exists():
        shutil.copy2(src, snapshot / name)

manifest = {
    "timestamp": time.time(),
    "archive_scanned": str(ARCH.relative_to(ROOT)),
    "current_canonical": str(CURRENT.relative_to(ROOT)),
    "candidate_count": len(candidates),
    "validated_count": sum(1 for x in candidates if x["validated"]),
    "documentation_candidates_promoted": len(promotable),
    "historical_executable_code": "not_blindly_activated",
    "runtime_activation": "verification_required",
    "continuity_model": [
        "archive",
        "candidate_registry",
        "validation",
        "promotion",
        "provenance",
        "snapshot",
        "runtime_verification"
    ]
}

(snapshot / "CONTINUITY_MANIFEST.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

REPORT.write_text(
f"""# IMA Continuity Report

Generated: {time.ctime()}

## Pipeline

Archive → Candidate Registry → Validation → Promotion → Provenance → Snapshot → Runtime Verification

## Results

- Archive candidates scanned: {len(candidates)}
- Validated candidates: {sum(1 for x in candidates if x["validated"])}
- Documentation/metadata candidates promoted: {len(promotable)}
- Historical executable code blindly activated: NO

## Runtime rule

Historical executable code remains inactive until independently verified
against the current runtime and explicitly promoted.

## Continuity rule

Verified identity, mission, principles, knowledge, provenance, safety,
and lessons may survive implementation changes.

The current implementation remains a generation, not the entirety of IMA.
""",
encoding="utf-8"
)

print("=== IMA CONTINUITY PROMOTION ===")
print("[OK] archive scanned")
print("[OK] candidate registry generated")
print("[OK] static validation completed")
print("[OK] provenance recorded")
print("[OK] continuity snapshot created")
print("[OK] historical executable code NOT blindly activated")
print("[OK] runtime activation remains verification-gated")
print(f"[OK] candidates: {len(candidates)}")
print(f"[OK] validated: {sum(1 for x in candidates if x['validated'])}")
print(f"[OK] documentation promoted: {len(promotable)}")
print(f"[OK] report: {REPORT.relative_to(ROOT)}")
