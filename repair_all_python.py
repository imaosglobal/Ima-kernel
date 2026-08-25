import ast
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime

ROOT = pathlib.Path(".").resolve()
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / f".repair_backup_{STAMP}"

SKIP = {
    ".git", "venv", "__pycache__",
    "_archive_20260808", "external", "node_modules"
}

def parse_ok(text, name):
    try:
        ast.parse(text, filename=name)
        return True
    except SyntaxError:
        return False

def broken_files():
    result = []
    for p in ROOT.rglob("*.py"):
        rel = p.relative_to(ROOT)
        if any(x in rel.parts for x in SKIP):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if not parse_ok(text, str(rel)):
            result.append(rel)
    return result

def git(cmd, cwd):
    return subprocess.run(
        ["git", *cmd],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

def repo_root(path):
    r = git(["rev-parse", "--show-toplevel"], path.parent)
    if r.returncode:
        return None
    return pathlib.Path(r.stdout.decode().strip()).resolve()

def find_valid_history(repo, rel):
    r = git(
        ["log", "--all", "--format=%H", "--", str(rel)],
        repo
    )

    if r.returncode:
        return None

    commits = r.stdout.decode(errors="replace").splitlines()

    for commit in commits:
        x = git(["show", f"{commit}:{rel}"], repo)
        if x.returncode:
            continue

        text = x.stdout.decode("utf-8", errors="replace")

        if parse_ok(text, str(rel)):
            return commit, text

    return None

broken = broken_files()

print("=== IMA FULL PYTHON REPAIR ===")
print("BROKEN BEFORE:", len(broken))
print("BACKUP:", BACKUP)

BACKUP.mkdir(parents=True, exist_ok=True)

repaired = []
unresolved = []

for rel in broken:
    path = ROOT / rel

    # Always preserve the current file first.
    dst = BACKUP / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)

    repo = repo_root(path)

    if repo is None:
        print("[UNRESOLVED] no git repo:", rel)
        unresolved.append((rel, "no git repo"))
        continue

    try:
        gitrel = path.resolve().relative_to(repo)
    except ValueError:
        unresolved.append((rel, "outside repo"))
        continue

    found = find_valid_history(repo, gitrel)

    if found is None:
        print("[UNRESOLVED] no valid historical version:", rel)
        unresolved.append((rel, "no valid historical version"))
        continue

    commit, text = found
    path.write_text(text, encoding="utf-8")

    print(f"[REPAIRED] {rel} <- {commit[:12]}")
    repaired.append(rel)

remaining = broken_files()

print()
print("=== RESULT ===")
print("BEFORE:", len(broken))
print("REPAIRED:", len(repaired))
print("UNRESOLVED:", len(unresolved))
print("REMAINING BROKEN:", len(remaining))

if unresolved:
    print()
    print("=== UNRESOLVED ===")
    for rel, reason in unresolved:
        print(rel, "|", reason)

if remaining:
    print()
    print("=== STILL BROKEN ===")
    for rel in remaining:
        print(rel)

report = BACKUP / "repair_report.txt"

with report.open("w", encoding="utf-8") as f:
    f.write(f"Before: {len(broken)}\n")
    f.write(f"Repaired: {len(repaired)}\n")
    f.write(f"Unresolved: {len(unresolved)}\n")
    f.write(f"Remaining: {len(remaining)}\n\n")

    f.write("REPAIRED\n")
    for x in repaired:
        f.write(f"{x}\n")

    f.write("\nUNRESOLVED\n")
    for x, reason in unresolved:
        f.write(f"{x} | {reason}\n")

    f.write("\nREMAINING\n")
    for x in remaining:
        f.write(f"{x}\n")

print()
print("REPORT:", report)

if remaining:
    sys.exit(2)
