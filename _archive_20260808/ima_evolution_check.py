from pathlib import Path
import json
import time
import hashlib
import importlib
import shutil

ROOT = Path(".")
REPORT = Path(".ima/ima_evolution_report.json")
BACKUP = Path(".ima/evolution_backups")

BACKUP.mkdir(parents=True, exist_ok=True)

modules = [
    "ima_master_runtime",
    "ima_brain",
    "brain_sync",
    "learning.ima_learning_loop",
    "learning.learning_memory",
    "learning.knowledge_expander",
    "learning.meta_orchestrator",
    "learning.knowledge_answer_builder"
]

report = {
    "system":"IMA",
    "time":time.time(),
    "modules":{},
    "files":{},
    "recommendations":[]
}

for m in modules:
    try:
        importlib.import_module(m)
        report["modules"][m]="OK"
    except Exception as e:
        report["modules"][m]="FAIL: "+str(e)

important = [
    "ima_master_runtime.py",
    "ima_brain.py",
    "brain_sync.py",
    "learning/learning_memory.json",
    "learning/learning_patterns.json"
]

for f in important:
    p=Path(f)
    if p.exists():
        report["files"][f]={
            "size":p.stat().st_size,
            "sha256":hashlib.sha256(p.read_bytes()).hexdigest()
        }
    else:
        report["files"][f]="MISSING"

if "learning.knowledge_answer_builder" not in report["modules"]:
    report["recommendations"].append(
        "חסר Knowledge Answer Builder"
    )

if report["modules"].get("brain_sync")!="OK":
    report["recommendations"].append(
        "חיבור Brain Sync דורש תיקון"
    )

report["recommendations"] += [
    "לאחד זיכרון ראשי וזיכרון דפוסים",
    "להוסיף בדיקת איכות תשובות",
    "להוסיף מחזור שיפור מבוקר",
    "לשמור רק מוח מרכזי אחד"
]

REPORT.write_text(
    json.dumps(
        report,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)

