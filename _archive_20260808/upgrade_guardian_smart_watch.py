from pathlib import Path
import json

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "def smart_diff" not in text:

    insert = r'''

def smart_diff():

    state = Path(".ima/guardian/smart_state.json")

    if not state.exists():
        return []

    old = json.loads(state.read_text(encoding="utf8"))
    changed = []

    for f, old_time in old.items():
        p = Path(f)
        if p.exists():
            try:
                if p.stat().st_mtime != old_time:
                    changed.append(f)
            except:
                pass

    return changed


def update_smart_state():

    state = Path(".ima/guardian/smart_state.json")
    data = {}

    for folder in ["ima","learning","runtime","api"]:
        p = Path(folder)
        if p.exists():
            for f in p.rglob("*.py"):
                if ".git" not in str(f):
                    try:
                        data[str(f)] = f.stat().st_mtime
                    except:
                        pass

    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(
        json.dumps(data, indent=2),
        encoding="utf8"
    )

'''

    text = text.replace(
        "def run_cycle():",
        insert + "\ndef run_cycle():"
    )


text = text.replace(
cycle()''',

changed = smart_diff()

cycle()

update_smart_state()'''
)

if "import json" not in text:
    text = "import json\n" + text

p.write_text(text, encoding="utf8")

