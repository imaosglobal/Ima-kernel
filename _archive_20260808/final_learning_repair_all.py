from pathlib import Path
import re
import shutil
import subprocess
import time

ROOT = Path("learning")

print("=== IMA FINAL LEARNING REPAIR ===")

# 1. backup
backup = Path(f"learning_backup_final_clean_{int(time.time())}")
shutil.copytree(ROOT, backup)
print("[BACKUP]", backup)


# 2. remove broken backup python files
removed = 0
for p in ROOT.rglob("*.py"):
    name = p.name
    if any(x in name for x in [
        ".before_compile_fix",
        ".before_import_cleanup",
        ".backup_fix_pipeline",
        ".tmp"
    ]):
        p.unlink()
        removed += 1

print("[REMOVED BACKUPS]", removed)


# 3. fix malformed imports in active files
patterns = [
    (
        r"from learning\.source_manager from learning\.sources\.html_extractor import extract_text",
        "from learning.source_manager import source_status\nfrom learning.sources.html_extractor import extract_text"
    ),
    (
        r"from pathlib from learning\.sources\.html_extractor import extract_text",
        "from pathlib import Path\nfrom learning.sources.html_extractor import extract_text"
    )
]

fixed = 0

for p in ROOT.rglob("*.py"):
    text = p.read_text(encoding="utf8")

    old = text

    for a,b in patterns:
        text = re.sub(a,b,text)

    if text != old:
        p.write_text(text,encoding="utf8")
        fixed += 1
        print("[FIXED]",p)

print("[IMPORT FIXES]",fixed)


# 4. compile active python only
print("[COMPILE]")

failed=[]

for p in ROOT.rglob("*.py"):
    if any(x in p.name for x in [
        ".before_",
        ".backup",
        ".tmp"
    ]):
        continue

    r=subprocess.run(
        ["python3","-m","py_compile",str(p)],
        capture_output=True,
        text=True
    )

    if r.returncode:
        failed.append((p,r.stderr))


if failed:
    print("[FAILED]")
    for p,e in failed:
        print("\n",p)
        print(e)
else:
    print("[ALL PYTHON OK]")


# 5. source test
print("[SOURCE STATUS]")

try:
    from learning.source_manager import source_status

    for s in source_status():
        print("-",s)

except Exception as e:
    print("[STATUS ERROR]",e)


print("=== FINAL REPAIR COMPLETE ===")
