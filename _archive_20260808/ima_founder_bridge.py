import json
from datetime import datetime

STATUS = {
    "identity": "IMA Founder Bridge",
    "created": str(datetime.now()),
    "connected": False
}

def connect():
    try:
        from founder.executive_ai.advisor.founder_advisor import advise

        STATUS["connected"] = True
        STATUS["advisor"] = True

        return STATUS

    except Exception as e:
        STATUS["error"] = str(e)
        return STATUS


def ask_founder(context):
    try:
        from founder.executive_ai.advisor.founder_advisor import advise

        return advise(context)

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


def bridge_status():
    return STATUS
