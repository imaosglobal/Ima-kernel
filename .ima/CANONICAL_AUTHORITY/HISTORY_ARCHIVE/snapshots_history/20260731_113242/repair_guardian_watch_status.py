
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

if "def guardian_status" not in text:

    insert = r'''

def guardian_status():

    from pathlib import Path

    print("=== IMA GUARDIAN WATCH STATUS ===")

    checks = {
        "controller": Path("ima_guardian_controller.py").exists(),
        "master": Path("ima_guardian_master.py").exists(),
        "policy": Path(".ima/CANONICAL_AUTHORITY/root_policy.json").exists(),
        "history": Path(".ima/guardian/history.jsonl").exists(),
        "smart_state": Path(".ima/guardian/smart_state.json").exists()
    }

    for k,v in checks.items():
        print(k + ":", v)

'''

    text = text.replace(
        "def run_cycle():",
        insert + "\ndef run_cycle():"
    )

    p.write_text(text, encoding="utf8")

    print("[OK] guardian_status restored")

else:
    print("[OK] guardian_status already exists")
