#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA VERSION UPGRADE LAYER ==="

mkdir -p product/version
mkdir -p .ima/upgrade_history

cat > product/version/version_manager.py <<'PY'
import json
import time
from pathlib import Path

VERSION_FILE = Path(
    "product/version/current_version.json"
)

def current():
    if VERSION_FILE.exists():
        return json.loads(
            VERSION_FILE.read_text()
        )

    return {
        "product": "IMA",
        "version": "1.0",
        "channel": "stable",
        "time": time.time()
    }


def upgrade(new_version):
    data = {
        "product": "IMA",
        "version": new_version,
        "channel": "stable",
        "upgraded": time.time()
    }

    VERSION_FILE.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    Path(
        ".ima/upgrade_history"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        ".ima/upgrade_history/"
        + new_version.replace(".","_")
        + ".json"
    ).write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    return data


if __name__ == "__main__":
PY


cat > product/version/upgrade_registry.json <<'JSON'
{
  "system": "IMA",
  "version_control": true,
  "migration": true,
  "rollback": true,
  "compatibility": "gateway_based",
  "core_modification": false
}
JSON


python3 - <<'PY'
from product.version.version_manager import current
PY


echo "=== VERSION UPGRADE LAYER READY ==="

