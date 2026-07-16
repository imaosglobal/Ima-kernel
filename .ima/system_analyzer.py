
from pathlib import Path
import json,time

REPORT=Path(".ima/self_improvement_report.json")
OUT=Path(".ima/system_analysis.json")

def analyze():

    report=json.loads(
        REPORT.read_text(encoding="utf-8")
    )

    analysis={
        "time":time.time(),
        "health":{
            "existing":len(report.get("existing",[])),
            "missing":len(report.get("missing",[]))
        },
        "priorities":[]
    }

    for item in report.get("missing",[]):
        analysis["priorities"].append({
            "issue":"missing_component",
            "target":item,
            "action":"create_or_define"
        })

    analysis["priorities"].append({
        "issue":"learning",
        "action":"connect lessons to decisions"
    })

    OUT.write_text(
        json.dumps(
            analysis,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return analysis

if __name__=="__main__":
    print(json.dumps(analyze(),ensure_ascii=False,indent=2))
