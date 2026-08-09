
from pathlib import Path
import sys

sys.path.insert(
    0,
    str(Path('.ima/CANONICAL_AUTHORITY'))
)

from policy_loader import load_root_policy

ROOT_POLICY = load_root_policy()


from pathlib import Path
import json

policy = Path(".ima/CANONICAL_AUTHORITY/root_policy.json")
policy.parent.mkdir(parents=True, exist_ok=True)

data = {
    "mode": "smart_incremental",
    "rules": {
        "scan_only_changed_files": True,
        "skip_master_when_target_ok": True,
        "repair_before_master": True,
        "compile_after_repair": True,
        "protect_guardian_files": True,
        "auto_commit_verified_changes": True
    },
    "protected": [
        "ima_guardian_watch.py",
        "ima_guardian_self_repair.py",
        "ima_guardian_master.py",
        "ima_guardian_controller.py"
    ]
}

policy.write_text(
    json.dumps(data, indent=2),
    encoding="utf8"
)

print("[OK] guardian policy lock created")
