import json
from pathlib import Path

from .outgoing_queue import pending


def status():

    return {
        "bridge":"online",
        "pending_reports":len(
            pending()
        )
    }


if __name__=="__main__":
    print(
        json.dumps(
            status(),
            indent=2,
            ensure_ascii=False
        )
    )
