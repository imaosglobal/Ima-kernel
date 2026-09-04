#!/usr/bin/env python3
"""
IMA Canonical Git Guard
Blocks autonomous Git operations when secrets or unsafe files are detected.
"""

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]

BLOCKED_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "service-account.json",
}

BLOCKED_PATTERNS = (
    r"(^|/)\.env($|\.)",
    r"(^|/).*secret.*",
    r"(^|/).*credential.*",
    r"(^|/).*password.*",
    r"(^|/).*token.*",
    r"(^|/).*private.*key.*",
    r"(^|/).*api[_-]?key.*",
)

SECRET_PATTERNS = (
    r"sk-[A-Za-z0-9_-]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"AKIA[0-9A-Z]{16}",
)

def git_status():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()

def suspicious_path(path):
    name = Path(path).name.lower()

    if name in {x.lower() for x in BLOCKED_NAMES}:
        return True

    normalized = str(path).replace("\\", "/").lower()

    return any(
        re.search(pattern, normalized, re.IGNORECASE)
        for pattern in BLOCKED_PATTERNS
    )

def contains_secret(path):
    p = ROOT / path

    if not p.is_file():
        return False

    try:
        if p.stat().st_size > 2 * 1024 * 1024:
            return False

        text = p.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return False

    return any(
        re.search(pattern, text)
        for pattern in SECRET_PATTERNS
    )

def check():
    blocked = []

    for line in git_status():
        if len(line) < 4:
            continue

        path = line[3:].strip()

        if " -> " in path:
            path = path.split(" -> ", 1)[-1]

        if suspicious_path(path):
            blocked.append((path, "blocked filename"))
            continue

        if contains_secret(path):
            blocked.append((path, "secret pattern detected"))

    if blocked:
        print("IMA_GIT_GUARD=BLOCK")
        for path, reason in blocked:
            print(f"BLOCKED: {path} [{reason}]")
        return False

    print("IMA_GIT_GUARD=PASS")
    print("No blocked filenames or detected secret patterns.")
    return True

if __name__ == "__main__":
    sys.exit(0 if check() else 1)
