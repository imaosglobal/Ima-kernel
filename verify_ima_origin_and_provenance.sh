#!/data/data/com.termux/files/usr/bin/bash

set -Eeuo pipefail

BASE="$HOME/ima_kernel"
OUT="$BASE/.ima/provenance_audit"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT="$OUT/IMA_ORIGIN_PROVENANCE_AUDIT_$STAMP.md"
JSON="$OUT/IMA_ORIGIN_PROVENANCE_AUDIT_$STAMP.json"

mkdir -p "$OUT"

export BASE OUT REPORT JSON STAMP

python3 - <<'PY'
import os, json, hashlib, subprocess, re
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(os.environ["BASE"]).resolve()
OUT = Path(os.environ["OUT"]).resolve()
REPORT = Path(os.environ["REPORT"]).resolve()
JSON_OUT = Path(os.environ["JSON"]).resolve()
STAMP = os.environ["STAMP"]

def run(cmd, cwd=BASE):
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30
        )
        return {
            "returncode": p.returncode,
            "output": p.stdout[-20000:]
        }
    except Exception as e:
        return {
            "returncode": -1,
            "output": str(e)
        }

def exists(rel):
    return (BASE / rel).exists()

def find_files(patterns, max_count=500):
    found = []
    for pattern in patterns:
        try:
            found.extend(BASE.glob(pattern))
        except Exception:
            pass
    unique = []
    seen = set()
    for p in found:
        try:
            r = p.resolve()
            if r not in seen and r.is_file():
                seen.add(r)
                unique.append(r)
        except Exception:
            pass
    return [str(x.relative_to(BASE)) for x in unique[:max_count]]

def sha256(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                h.update(block)
        return h.hexdigest()
    except Exception:
        return None

def read_text(rel, limit=30000):
    p = BASE / rel
    try:
        return p.read_text(encoding="utf-8", errors="replace")[:limit]
    except Exception:
        return None

def contains_any(text, terms):
    if not text:
        return []
    low = text.lower()
    return [t for t in terms if t.lower() in low]

data = {
    "audit": {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "base": str(BASE),
        "mode": "READ_ONLY",
        "mutated_existing_files": False
    },
    "identity_and_origin": {},
    "canonical_authority": {},
    "git_provenance": {},
    "cryptographic_provenance": {},
    "timestamps": {},
    "history": {},
    "registries": {},
    "consistency": {},
    "verdict": {}
}

# --------------------------------------------------
# IDENTITY / ORIGIN
# --------------------------------------------------

identity_candidates = find_files([
    ".ima/**/*identity*.json",
    ".ima/**/*identity*.md",
    ".ima/**/*founder*.json",
    ".ima/**/*founder*.md",
    ".ima/**/*ori*.json",
    ".ima/**/*ori*.md",
    "**/*origin*.json",
    "**/*origin*.md",
    "**/*creator*.json",
    "**/*creator*.md",
    "**/*vision*.json",
    "**/*vision*.md",
    "**/*manifest*.json"
])

identity_hits = []

terms = [
    "Ori Cohen",
    "אורי כהן",
    "IMA",
    "founder",
    "creator",
    "origin",
    "vision",
    "author",
    "creator",
    "יוצר",
    "מייסד",
    "חזון"
]

for rel in identity_candidates:
    text = read_text(rel)
    hits = contains_any(text, terms)
    if hits:
        identity_hits.append({
            "file": rel,
            "signals": hits,
            "sha256": sha256(BASE / rel)
        })

data["identity_and_origin"] = {
    "candidate_files": identity_candidates,
    "files_with_identity_signals": identity_hits,
    "status": "FOUND" if identity_hits else "NOT_FOUND"
}

# --------------------------------------------------
# CANONICAL AUTHORITY
# --------------------------------------------------

canonical = BASE / ".ima" / "CANONICAL_AUTHORITY"

canonical_files = []
if canonical.exists():
    for p in canonical.rglob("*"):
        if p.is_file():
            try:
                canonical_files.append({
                    "file": str(p.relative_to(BASE)),
                    "size": p.stat().st_size,
                    "sha256": sha256(p)
                })
            except Exception:
                pass

data["canonical_authority"] = {
    "path": str(canonical),
    "exists": canonical.exists(),
    "file_count": len(canonical_files),
    "files": canonical_files[:1000]
}

# --------------------------------------------------
# GIT PROVENANCE
# --------------------------------------------------

git = {}

git["is_repository"] = (BASE / ".git").exists()

if git["is_repository"]:
    git["remote"] = run(["git", "remote", "-v"])
    git["status"] = run(["git", "status", "--short"])
    git["log"] = run([
        "git", "log",
        "--date=iso-strict",
        "--pretty=format:%H|%aI|%an|%ae|%s",
        "-n", "100"
    ])
    git["first_commit"] = run([
        "git", "rev-list", "--max-parents=0", "HEAD"
    ])
    git["branches"] = run([
        "git", "branch", "-a"
    ])
    git["tags"] = run([
        "git", "tag", "--list"
    ])
    git["signed_log"] = run([
        "git", "log",
        "--show-signature",
        "-n", "20"
    ])

data["git_provenance"] = git

# --------------------------------------------------
# CRYPTOGRAPHIC PROVENANCE
# --------------------------------------------------

hash_files = find_files([
    "**/HASHES.sha256",
    "**/*.sha256",
    "**/*hash*.json",
    "**/*hash*.txt",
    ".ima/**/*integrity*.json",
    ".ima/**/*integrity*.md",
    ".ima/**/*chain*.json",
    ".ima/**/*chain*.md",
    ".ima/**/*lock*.json"
], max_count=1000)

hash_records = []

for rel in hash_files:
    text = read_text(rel, 100000)
    hash_records.append({
        "file": rel,
        "sha256": sha256(BASE / rel),
        "mentions_sha256": bool(text and "sha256" in text.lower()),
        "mentions_chain": bool(text and "chain" in text.lower()),
        "mentions_canonical": bool(text and "canonical" in text.lower())
    })

data["cryptographic_provenance"] = {
    "candidate_hash_files": hash_records,
    "status": "FOUND" if hash_records else "NOT_FOUND"
}

# --------------------------------------------------
# TIMESTAMPS
# --------------------------------------------------

timestamp_files = find_files([
    ".ima/releases/**/*",
    ".ima/snapshots/**/*",
    ".ima/backups/**/*",
    ".ima/archive_final/**/*"
], max_count=1000)

timestamp_records = []

for rel in timestamp_files[:1000]:
    try:
        p = BASE / rel
        st = p.stat()
        timestamp_records.append({
            "file": rel,
            "mtime_utc": datetime.fromtimestamp(
                st.st_mtime,
                timezone.utc
            ).isoformat()
        })
    except Exception:
        pass

data["timestamps"] = {
    "timestamped_items_found": len(timestamp_records),
    "items": timestamp_records[:1000]
}

# --------------------------------------------------
# HISTORY
# --------------------------------------------------

history_candidates = find_files([
    ".ima/**/*history*.json",
    ".ima/**/*history*.jsonl",
    ".ima/**/*evolution*.json",
    ".ima/**/*evolution*.jsonl",
    ".ima/**/*memory*.jsonl",
    ".ima/**/*timeline*.json",
    ".ima/**/*timeline*.md",
    "**/CHANGELOG*",
    "**/HISTORY*",
    "**/README*"
], max_count=1000)

data["history"] = {
    "candidate_files": history_candidates,
    "count": len(history_candidates)
}

# --------------------------------------------------
# REGISTRIES
# --------------------------------------------------

registry_candidates = find_files([
    ".ima/**/*registry*.json",
    "deployment/**/*registry*.json",
    "connectors/**/*registry*.json",
    "**/*policy*.json",
    "**/*manifest*.json"
], max_count=1000)

registry_records = []

for rel in registry_candidates:
    text = read_text(rel, 50000)
    registry_records.append({
        "file": rel,
        "sha256": sha256(BASE / rel),
        "has_canonical": bool(text and "canonical" in text.lower()),
        "has_policy": bool(text and "policy" in text.lower()),
        "has_ima": bool(text and "ima" in text.lower())
    })

data["registries"] = {
    "files": registry_records,
    "count": len(registry_records)
}

# --------------------------------------------------
# CONSISTENCY
# --------------------------------------------------

all_identity_text = []

for item in identity_hits:
    text = read_text(item["file"], 30000)
    if text:
        all_identity_text.append(text)

combined = "\n".join(all_identity_text)

consistency = {
    "creator_name_mentions": {
        "Ori Cohen": combined.lower().count("ori cohen"),
        "אורי כהן": combined.count("אורי כהן")
    },
    "ima_mentions": combined.lower().count("ima"),
    "conflicting_creator_names": []
}

names = set(
    re.findall(
        r"(?:founder|creator|author|מייסד|יוצר)\s*[:=]\s*[\"']?([^\"'\n,}]+)",
        combined,
        flags=re.IGNORECASE
    )
)

consistency["creator_claims_found"] = sorted(names)

data["consistency"] = consistency

# --------------------------------------------------
# VERDICT
# --------------------------------------------------

checks = {
    "identity_or_origin_documented": bool(identity_hits),
    "canonical_authority_exists": canonical.exists(),
    "git_history_exists": bool(git.get("is_repository")),
    "hash_or_integrity_artifacts_exist": bool(hash_records),
    "timestamped_history_exists": bool(timestamp_records),
    "historical_artifacts_exist": bool(history_candidates),
    "registries_exist": bool(registry_candidates)
}

score = sum(1 for x in checks.values() if x)
total = len(checks)

data["verdict"] = {
    "checks": checks,
    "score": score,
    "total": total,
    "percentage": round((score / total) * 100, 1),
    "interpretation": (
        "PROVENANCE_SYSTEM_PRESENT"
        if score >= 6
        else "PARTIAL_PROVENANCE"
        if score >= 3
        else "INSUFFICIENT_PROVENANCE"
    )
}

JSON_OUT.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

lines = []

lines.append("# IMA — Origin & Provenance Audit")
lines.append("")
lines.append(f"- Audit time UTC: `{data['audit']['timestamp_utc']}`")
lines.append(f"- Base: `{BASE}`")
lines.append("- Mode: `READ_ONLY`")
lines.append("- Existing files modified: `NO`")
lines.append("")

lines.append("## Verdict")
lines.append("")
lines.append(f"**{data['verdict']['interpretation']}**")
lines.append("")
lines.append(
    f"Score: **{data['verdict']['score']}/{data['verdict']['total']} "
    f"({data['verdict']['percentage']}%)**"
)
lines.append("")

for k, v in checks.items():
    lines.append(f"- [{'x' if v else ' '}] {k}")

lines.append("")
lines.append("## Identity / Origin")
lines.append("")
lines.append(
    f"Status: **{data['identity_and_origin']['status']}**"
)
lines.append(
    f"Candidate files: {len(data['identity_and_origin']['candidate_files'])}"
)
lines.append(
    f"Files containing identity signals: "
    f"{len(data['identity_and_origin']['files_with_identity_signals'])}"
)
lines.append("")

for item in data["identity_and_origin"]["files_with_identity_signals"][:100]:
    lines.append(
        f"- `{item['file']}` — "
        f"{', '.join(item['signals'])}"
    )

lines.append("")
lines.append("## Canonical Authority")
lines.append("")
lines.append(
    f"Exists: **{data['canonical_authority']['exists']}**"
)
lines.append(
    f"Files: **{len(data['canonical_authority']['files'])}**"
)
lines.append("")

lines.append("## Git Provenance")
lines.append("")
lines.append(
    f"Repository: **{git.get('is_repository', False)}**"
)
lines.append("")

if git.get("remote"):
    lines.append("### Remote")
    lines.append("")
    lines.append("```")
    lines.append(git["remote"]["output"])
    lines.append("```")
    lines.append("")

if git.get("first_commit"):
    lines.append("### First Commit")
    lines.append("")
    lines.append("```")
    lines.append(git["first_commit"]["output"])
    lines.append("```")
    lines.append("")

if git.get("log"):
    lines.append("### Recent History")
    lines.append("")
    lines.append("```")
    lines.append(git["log"]["output"])
    lines.append("```")
    lines.append("")

lines.append("## Cryptographic / Integrity Evidence")
lines.append("")
lines.append(
    f"Candidate artifacts: "
    f"**{len(data['cryptographic_provenance']['candidate_hash_files'])}**"
)
lines.append("")

for item in data["cryptographic_provenance"]["candidate_hash_files"][:100]:
    lines.append(
        f"- `{item['file']}` — SHA256 `{item['sha256']}`"
    )

lines.append("")
lines.append("## Historical Evidence")
lines.append("")
lines.append(
    f"Historical candidate files: **{data['history']['count']}**"
)
lines.append("")

for rel in data["history"]["candidate_files"][:200]:
    lines.append(f"- `{rel}`")

lines.append("")
lines.append("## Consistency")
lines.append("")
lines.append(
    f"- Ori Cohen mentions: "
    f"{data['consistency']['creator_name_mentions']['Ori Cohen']}"
)
lines.append(
    f"- אורי כהן mentions: "
    f"{data['consistency']['creator_name_mentions']['אורי כהן']}"
)
lines.append(
    f"- IMA mentions in identity material: "
    f"{data['consistency']['ima_mentions']}"
)

if data["consistency"]["creator_claims_found"]:
    lines.append("")
    lines.append("Creator claims:")
    for name in data["consistency"]["creator_claims_found"]:
        lines.append(f"- `{name}`")

lines.append("")
lines.append("## Important Interpretation")
lines.append("")
lines.append(
    "This audit does not decide legal ownership or prove that every historical "
    "claim is true. It verifies what evidence is currently present inside the "
    "IMA project and whether the project contains a traceable provenance structure."
)
lines.append("")
lines.append(
    "The audit itself is a new evidence artifact. Its SHA-256 is printed below."
)

REPORT.write_text("\n".join(lines), encoding="utf-8")

    f"SCORE:   {data['verdict']['score']}/"
    f"{data['verdict']['total']} "
    f"({data['verdict']['percentage']}%)"
)
PY

echo
echo "=== AUDIT FILES ==="
ls -lh "$OUT"
echo
echo "=== LATEST REPORT ==="
ls -t "$OUT"/IMA_ORIGIN_PROVENANCE_AUDIT_*.md | head -1
