from pathlib import Path
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
