import json
import sys
from pathlib import Path


BASE=Path(".ima/self_awareness")
BRIDGE=BASE/"bridge"

sys.path.append(str(BASE))
sys.path.append(str(BRIDGE))


from auto_trigger import should_report


def run():

    if not should_report():
        return {
            "status":"no_trigger"
        }


    try:
        from report_generator import create_report
        from sender import send_pending


        report=create_report()

        sent=send_pending()


        return {
            "status":"completed",
            "report":report,
            "sent":sent
        }


    except Exception as e:

        return {
            "status":"error",
            "error":str(e)
        }


if __name__=="__main__":

    print(
        json.dumps(
            run(),
            indent=2,
            ensure_ascii=False
        )
    )
