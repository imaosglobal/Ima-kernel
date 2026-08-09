import json
from pathlib import Path
from datetime import datetime

from report_filter import filter_report


REPORTS=Path(".ima/self_awareness/reports.jsonl")
OUT=Path(".ima/self_awareness/outgoing_reports.jsonl")


def send_report():

    if not REPORTS.exists():
        return None


    lines=REPORTS.read_text().splitlines()

    if not lines:
        return None


    report=json.loads(
        lines[-1]
    )


    safe=filter_report(report)


    packet={
        "created":
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "destination":
        "external_bridge_pending",

        "payload":
        safe
    }


    with OUT.open("a") as f:
        f.write(
            json.dumps(
                packet,
                ensure_ascii=False
            )+"\n"
        )


    return packet


if __name__=="__main__":
    print(
        json.dumps(
            send_report(),
            indent=2,
            ensure_ascii=False
        )
    )
