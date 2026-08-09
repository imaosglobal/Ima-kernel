import json
from pathlib import Path
from datetime import datetime

try:
    from .outgoing_queue import pending, mark_sent
except ImportError:
    from outgoing_queue import pending, mark_sent


QUEUE=Path(".ima/self_awareness/outgoing_reports.jsonl")


def send_pending():

    items=pending()

    sent=0

    for item in items:
        packet={
            "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type":"bridge_delivery",
            "status":"ready",
            "payload":item
        }

        print(
            json.dumps(
                packet,
                ensure_ascii=False,
                indent=2
            )
        )

        mark_sent(item)
        sent+=1


    return {
        "sent":sent,
        "remaining":len(items)-sent
    }


if __name__=="__main__":
    print(
        json.dumps(
            send_pending(),
            ensure_ascii=False,
            indent=2
        )
    )
