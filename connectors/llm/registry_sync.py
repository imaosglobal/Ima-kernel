from pathlib import Path
import json
import time

from connectors.llm.provider_scanner import scan_all

REGISTRY=Path(".ima/llm_registry.json")


def sync():
    scan=scan_all()

    data={
        "time":time.time(),
        "identity":"IMA",
        "local_models":scan["local_models"],
        "cloud_providers":scan["cloud_providers"]
    }

    REGISTRY.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return data


if __name__=="__main__":
