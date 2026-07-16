
from pathlib import Path
import json,time

FILES=[
".ima/ledger.jsonl",
".ima/system_learning.jsonl",
".ima/feedback_loop.json",
"ima_master_runtime.py"
]

def review():

    result={
        "time":time.time(),
        "checks":{},
        "lessons":[]
    }

    for f in FILES:
        path=Path(f)
        result["checks"][f]=path.exists()

    if result["checks"].get("ima_master_runtime.py"):
        result["lessons"].append(
            "Keep runtime stable before adding features"
        )

    if result["checks"].get(".ima/ledger.jsonl"):
        result["lessons"].append(
            "Memory storage is available"
        )

    out=Path(".ima/self_review_report.json")
    out.write_text(
        json.dumps(result,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )

    with Path(".ima/system_learning.jsonl").open("a",encoding="utf-8") as f:
        f.write(
            json.dumps({
                "type":"SELF_REVIEW",
                "time":time.time(),
                "lessons":result["lessons"]
            },ensure_ascii=False)+"\n"
        )

    return result

if __name__=="__main__":
    print(json.dumps(review(),ensure_ascii=False,indent=2))
