from pathlib import Path
import shutil
import re
import json
from datetime import datetime

ROOT=Path(".")
REPORT=Path(".ima/self_awareness/bridge_audit_report.json")

files=[
    Path(".ima/observer/ima_observer.py"),
    Path(".ima/self_awareness/bridge/auto_report_cycle.py"),
    Path(".ima/self_awareness/bridge/auto_trigger.py"),
    Path(".ima/self_awareness/bridge/sender.py"),
    Path(".ima/self_awareness/report_generator.py"),
]

audit={}

for f in files:
    if f.exists():
        text=f.read_text(errors="ignore")
        audit[str(f)]={
            "exists":True,
            "run_refs":len(re.findall(r"\brun\(",text)),
            "bridge_refs":len(re.findall(r"bridge|BRIDGE",text,re.I)),
            "trigger_refs":len(re.findall(r"trigger|should_report",text)),
        }
    else:
        audit[str(f)]={
            "exists":False
        }


def backup(path):
    if path.exists():
        dst=Path(".ima/backups_bridge_auto_repair")
        dst.mkdir(parents=True,exist_ok=True)
        shutil.copy(path,dst/path.name)


# תיקון מרכז ההחלטה בלבד
cycle=Path(".ima/self_awareness/bridge/auto_report_cycle.py")

if cycle.exists():

    backup(cycle)

    text=cycle.read_text()

    if "from auto_trigger import should_report" not in text:
        print("WARNING: trigger import missing - not modified")

    else:
        print("AUTO REPORT GATE VERIFIED")


# בדיקת observer
observer=Path(".ima/observer/ima_observer.py")

if observer.exists():

    text=observer.read_text()

    if text.count("run_bridge_cycle()")>1:
        print("WARNING: duplicate bridge calls detected")

    else:
        print("OBSERVER BRIDGE CALL COUNT OK")


audit["time"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
audit["decision"]="audit_only_safe_mode"

REPORT.parent.mkdir(parents=True,exist_ok=True)

REPORT.write_text(
    json.dumps(
        audit,
        indent=2,
        ensure_ascii=False
    )
)

print(json.dumps(audit,indent=2,ensure_ascii=False))
print("BRIDGE AUDIT COMPLETE")
