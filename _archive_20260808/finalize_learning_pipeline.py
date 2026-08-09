from pathlib import Path
import shutil
import json
import os
import subprocess
import time

print("=== IMA FINAL LEARNING PIPELINE ===")

ROOT = Path("learning")

# 1. backup
backup = Path(f"learning_backup_final_{int(time.time())}")

if ROOT.exists():
    shutil.copytree(ROOT, backup)
    print("[BACKUP]", backup)


# 2. permissions
print("[FIX PERMISSIONS]")

for p in ROOT.rglob("*"):
    try:
        if p.is_file():
            os.chmod(p, 0o644)
    except:
        pass


# 3. registry cleanup

registry = Path("learning/sources/registry.json")

if registry.exists():

    data=json.loads(
        registry.read_text(encoding="utf8")
    )

    clean=[]
    seen=set()

    for s in data.get("sources",[]):

        name=s.get("name")

        if name and name not in seen:
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

    print("[REGISTRY]",len(clean))


# 4. extractor

extractor=Path(
"learning/sources/html_extractor.py"
)

if not extractor.exists():

    extractor.write_text(
'''
import re
from html import unescape

def extract_text(html):

    if not html:
        return ""

    html=re.sub(
        r"<script.*?</script>",
        "",
        html,
        flags=re.S
    )

    html=re.sub(
        r"<style.*?</style>",
        "",
        html,
        flags=re.S
    )

    html=re.sub(
        r"<[^>]+>",
        " ",
        html
    )

    html=unescape(html)

    return " ".join(html.split())[:5000]
''',
    encoding="utf8"
    )

    print("[EXTRACTOR CREATED]")


# 5. patch collectors automatically

print("[PATCH COLLECTORS]")

for p in ROOT.rglob("*.py"):

    try:
        text=p.read_text(encoding="utf8")

    except:
        continue


    if "content" in text and "extract_text" not in text:

        if "return" in text:

            text=text.replace(
                "import ",
                "from learning.sources.html_extractor import extract_text\nimport ",
                1
            )

            text=text.replace(
                '"content": content',
                '"content": extract_text(content)'
            )

            p.write_text(
                text,
                encoding="utf8"
            )

            print("[PATCHED]",p)


# 6. compile

print("[COMPILE]")

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
        print(f)

else:
    print("[ALL PYTHON OK]")


# 7. source status test

print("[SOURCE TEST]")

try:

    from learning.source_manager import source_status

    for s in source_status():
        print("-",s)

except Exception as e:

    print("[STATUS ERROR]",e)


print("=== PIPELINE COMPLETE ===")
