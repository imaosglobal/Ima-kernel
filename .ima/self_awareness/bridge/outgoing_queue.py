import json
from pathlib import Path
from datetime import datetime


QUEUE=Path(".ima/self_awareness/outgoing_reports.jsonl")
SENT=Path(".ima/self_awareness/sent_reports.jsonl")


def sent_keys():

    if not SENT.exists():
        return set()

    keys=set()

    for line in SENT.read_text().splitlines():
        try:
            item=json.loads(line)

            report=item.get("report",{})

            payload=json.dumps(
                report,
                sort_keys=True,
                ensure_ascii=False
            )

            keys.add(payload)

        except Exception:
            pass

    return keys



def pending():

    if not QUEUE.exists():
        return []

    sent=sent_keys()
    result=[]

    for line in QUEUE.read_text().splitlines():

        try:
            item=json.loads(line)

            key=json.dumps(
                item,
                sort_keys=True,
                ensure_ascii=False
            )

            if key not in sent:
                result.append(item)

        except Exception:
            pass

    return result



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
                "pending":len(pending())
            },
            indent=2,
            ensure_ascii=False
        )
    )
