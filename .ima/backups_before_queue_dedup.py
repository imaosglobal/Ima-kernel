import json
from pathlib import Path
from datetime import datetime


QUEUE=Path(".ima/self_awareness/outgoing_reports.jsonl")
SENT=Path(".ima/self_awareness/sent_reports.jsonl")


def pending():

    if not QUEUE.exists():
        return []

    return [
        json.loads(x)
        for x in QUEUE.read_text().splitlines()
    ]


def mark_sent(item):

    with SENT.open("a") as f:
        f.write(
            json.dumps(
                {
                    "sent":
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "report":item
                },
                ensure_ascii=False
            )+"\n"
        )


if __name__=="__main__":
    print(
        json.dumps(
            {
                "pending":
                len(pending())
            },
            indent=2,
            ensure_ascii=False
        )
    )
