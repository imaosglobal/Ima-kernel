import json
from datetime import datetime


def send(payload, url=None):

    packet={
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transport":"webhook",
        "destination":url or "not_configured",
        "payload":payload
    }

    return {
        "status":"prepared",
        "packet":packet
    }


if __name__=="__main__":
    print(
        json.dumps(
            send({"test":"IMA bridge"}),
            indent=2,
            ensure_ascii=False
        )
    )
