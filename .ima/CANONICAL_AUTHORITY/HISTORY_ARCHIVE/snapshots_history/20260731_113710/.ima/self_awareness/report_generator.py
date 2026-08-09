import json
from pathlib import Path
from datetime import datetime

from self_diagnosis import diagnose


REPORTS=Path(".ima/self_awareness/reports.jsonl")


def create_report():

    report={
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type":"system_report",
        "data":diagnose()
    }


    with REPORTS.open("a") as f:
        f.write(
            json.dumps(
                report,
                ensure_ascii=False
            )+"\n"
        )


    return report


if __name__=="__main__":
    print(
        json.dumps(
            create_report(),
            indent=2,
            ensure_ascii=False
        )
    )
