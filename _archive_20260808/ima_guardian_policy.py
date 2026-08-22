from pathlib import Path
import json

POLICY = Path(".ima/guardian/policy.json")

DEFAULT = {
    "active_paths": [
        "learning",
        "ima",
        "api",
        "runtime"
    ],
    "protected_paths": [
        ".ima/backups",
        ".ima/archive",
        "archive",
        "snapshots"
    ],
    "auto_fix": True,
    "auto_commit": True,
    "rollback_on_failure": True,
    "max_history_lines": 2000
}


def load_policy():
    if not POLICY.exists():
        POLICY.parent.mkdir(parents=True, exist_ok=True)
        POLICY.write_text(
            json.dumps(DEFAULT, indent=2),
            encoding="utf8"
        )
        return DEFAULT

    return json.loads(
        POLICY.read_text(encoding="utf8")
    )


def allowed(path):

    p = str(path)

    policy = load_policy()

    for blocked in policy["protected_paths"]:
        if blocked in p:
            return False

    for active in policy["active_paths"]:
        if p.startswith(active):
            return True

    return False


if __name__ == "__main__":
