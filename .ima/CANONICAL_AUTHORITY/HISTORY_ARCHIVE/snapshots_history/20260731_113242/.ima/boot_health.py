
import subprocess
import json,time
from pathlib import Path

def boot_check():

    report={
        "time":time.time(),
        "status":"checking",
        "tests":{}
    }

    try:
        subprocess.run(
            ["python3",".ima/self_review.py"],
            check=True,
            capture_output=True
        )
        report["tests"]["self_review"]="ok"

    except Exception as e:
        report["tests"]["self_review"]=str(e)

    report["status"]="ready"

    Path(".ima/boot_health.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )

    return report

if __name__=="__main__":
    print(json.dumps(boot_check(),ensure_ascii=False,indent=2))
