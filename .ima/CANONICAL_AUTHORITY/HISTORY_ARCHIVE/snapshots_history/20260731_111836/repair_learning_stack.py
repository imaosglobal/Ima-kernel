from pathlib import Path
import shutil
import json
import os
import time
import subprocess

ROOT = Path("learning")

print("=== IMA LEARNING STACK REPAIR ===")

# 1. backup
backup = Path(f"learning_backup_repair_{int(time.time())}")
if ROOT.exists():
    shutil.copytree(ROOT, backup)
    print("[BACKUP]", backup)

# 2. permissions
print("[PERMISSIONS]")
for p in ROOT.rglob("*"):
    try:
        if p.is_file():
            os.chmod(p, 0o644)
    except:
        pass

# 3. clean registry duplicates
registry = Path("learning/sources/registry.json")

if registry.exists():
    data = json.loads(registry.read_text(encoding="utf8"))

    clean=[]
    seen=set()

    for s in data.get("sources",[]):
        name=s.get("name")

        if name not in seen:
            seen.add(name)
            clean.append(s)

    data["sources"]=clean

    registry.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    print("[REGISTRY CLEAN]",len(clean))


# 4. create extractor
extractor = Path("learning/sources/html_extractor.py")

if not extractor.exists():

    extractor.write_text(
'''import re
from html import unescape

def extract_text(html):

    if not html:
        return ""

    html = re.sub(
        r"<script.*?</script>",
        "",
        html,
        flags=re.S
    )

    html = re.sub(
        r"<style.*?</style>",
        "",
        html,
        flags=re.S
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        html
    )

    text = unescape(text)

    text = " ".join(text.split())

    return text[:5000]
''',
        encoding="utf8"
    )

    print("[EXTRACTOR CREATED]")


# 5. compile
print("[COMPILE TEST]")

failed=[]

for p in ROOT.rglob("*.py"):

    r=subprocess.run(
        [
            "python3",
            "-m",
            "py_compile",
            str(p)
        ],
        capture_output=True
    )

    if r.returncode:
        failed.append(str(p))


if failed:
    print("[FAILED]")
    for f in failed:
        print("-",f)
else:
    print("[ALL PYTHON OK]")


print("=== REPAIR COMPLETE ===")
