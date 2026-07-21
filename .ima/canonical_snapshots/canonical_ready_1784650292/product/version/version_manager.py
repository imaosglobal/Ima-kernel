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
    print(json.dumps(current(), indent=2))
