
from pathlib import Path
import sys

sys.path.insert(
    0,
    str(Path('.ima/CANONICAL_AUTHORITY'))
)

from policy_loader import load_root_policy

ROOT_POLICY = load_root_policy()


from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "guardian_policy_check" not in text:

    addition = r'''

def guardian_policy_check():
    import json

    p = Path(".ima/CANONICAL_AUTHORITY/root_policy.json")

    if not p.exists():
        print("[POLICY MISSING]")
        return False

    try:
        data=json.loads(p.read_text(encoding="utf8"))
        return data.get("rules",{}).get(
            "scan_only_changed_files",
            False
        )
    except Exception:
        return False
'''

    text = addition + "\n" + text


old = '''def run_cycle():
    print("\\n=== GUARDIAN AUTO CYCLE ===")
'''

new = '''def run_cycle():
    print("\\n=== GUARDIAN AUTO CYCLE ===")

    if not guardian_policy_check():
        print("[POLICY BLOCK]")
        return
'''

if old in text:
    text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")

print("[OK] guardian policy gate connected")
