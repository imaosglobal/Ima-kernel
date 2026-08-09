from pathlib import Path
import json

files = [
    "ima_guardian_core.py",
    "ima_guardian_watch.py",
    "ima_guardian_master.py"
]

for name in files:
    p = Path(name)

    if not p.exists():
        continue

    text = p.read_text(encoding="utf8")

    marker = "# IMA_SMART_MODE"

    if marker in text:
        continue

    addition = r'''

# IMA_SMART_MODE

from pathlib import Path
import json
import time


SMART_STATE = Path(".ima/guardian/smart_state.json")


def smart_snapshot():

    result = {}

    for folder in [
        "ima",
        "learning",
        "runtime",
        "api"
    ]:

        p = Path(folder)

        if not p.exists():
            continue

        for f in p.rglob("*.py"):

            if ".git" in str(f):
                continue

            if "__pycache__" in str(f):
                continue

            try:
                result[str(f)] = f.stat().st_mtime
            except:
                pass

    return result


def smart_changed():

    current = smart_snapshot()

    old = {}

    if SMART_STATE.exists():

        try:
            old=json.loads(
                SMART_STATE.read_text()
            )

        except:
            pass


    SMART_STATE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    SMART_STATE.write_text(
        json.dumps(current)
    )


    return [
        x for x in current
        if old.get(x)!=current[x]
    ]
'''

    p.write_text(
        text + addition,
        encoding="utf8"
    )

    print("[OK]", name)

print("[OK] smart mode installed")
