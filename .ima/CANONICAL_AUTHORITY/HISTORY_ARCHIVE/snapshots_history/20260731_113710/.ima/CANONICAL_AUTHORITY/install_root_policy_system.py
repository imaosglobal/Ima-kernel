from pathlib import Path
import json
import hashlib
from datetime import datetime

ROOT = Path(".ima")
AUTH = ROOT / "CANONICAL_AUTHORITY"

AUTH.mkdir(parents=True, exist_ok=True)

timestamp = datetime.utcnow().isoformat()

# backup
backup = AUTH / "pre_root_policy_backup.json"

existing = {}

targets = [
    "baseline.json",
    "stable_baseline.json",
    "governance/final_governance_lock.json",
    "governance/canonical_architecture.json",
    "governance/canonical_map.json",
    "releases/canonical/canonical_manifest.json",
    "runtime/canonical_system_lock.json",
    "runtime/canonical_manifest.json",
    "runtime/canonical_boot_guard.json",
    "policy/universal_human_flourishing_policy.json",
    "guardian/policy.json"
]

for t in targets:
    p = ROOT / t
    existing[t] = {
        "exists": p.exists(),
        "sha256": hashlib.sha256(
            p.read_bytes()
        ).hexdigest()
        if p.exists()
        else None
    }

backup.write_text(
    json.dumps(
        {
            "created": timestamp,
            "existing": existing
        },
        indent=2
    ),
    encoding="utf-8"
)


root_policy = {
    "authority": "IMA_ROOT_POLICY",
    "version": "1.0",
    "created": timestamp,

    "role": "single canonical policy authority",

    "inherits_from": [
        "baseline.json",
        "policy/universal_human_flourishing_policy.json"
    ],

    "rules": {
        "all_changes_require_validation": True,
        "all_runtime_components_must_register": True,
        "history_is_immutable": True,
        "snapshots_are_history_only": True,
        "runtime_is_not_allowed_to_modify_policy": True
    },

    "connected_sources": existing
}


(AUTH / "root_policy.json").write_text(
    json.dumps(root_policy, indent=2),
    encoding="utf-8"
)


loader = AUTH / "policy_loader.py"

loader.write_text(
'''from pathlib import Path
import json

ROOT = Path(".ima/CANONICAL_AUTHORITY")

def load_root_policy():
    p = ROOT / "root_policy.json"

    if not p.exists():
        raise RuntimeError(
            "IMA ROOT POLICY MISSING"
        )

    return json.loads(
        p.read_text(
            encoding="utf-8"
        )
    )


if __name__ == "__main__":
    print(
        json.dumps(
            load_root_policy(),
            indent=2
        )
    )
''',
encoding="utf-8"
)


print("ROOT POLICY INSTALLED")
print("Authority:")
print(AUTH / "root_policy.json")
print("Loader:")
print(loader)
print("Backup:")
print(backup)
