
from pathlib import Path
import json,time

FEEDBACK=Path(".ima/feedback_loop.json")
LESSONS=Path(".ima/system_learning.jsonl")


def sync_feedback():

    if not FEEDBACK.exists():
        return

    data=json.loads(
        FEEDBACK.read_text(encoding="utf-8")
    )

    history=data.get("history",[])

    if not history:
        return

    with LESSONS.open("a",encoding="utf-8") as f:

        for item in history[-5:]:

            lesson={
                "type":"AUTO_LESSON",
                "time":time.time(),
                "lesson":{
                    "action":item.get("action"),
                    "result":item.get("status"),
                    "details":item.get("details")
                }
            }

            f.write(
                json.dumps(
                    lesson,
                    ensure_ascii=False
                )+"\n"
            )


if __name__=="__main__":
    sync_feedback()
    print("[OK] feedback synced to learning")
