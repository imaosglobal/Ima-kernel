from pathlib import Path
import subprocess
import json
from datetime import datetime

ROOT=Path(".")
GUARD=ROOT/".ima_guardian"

GUARD.mkdir(exist_ok=True)

# git init אם אין
if not (ROOT/".git").exists():
    subprocess.run(["git","init"])

# ignore רעשים
gitignore=ROOT/".gitignore"

ignore=[
".ima/backups/",
".ima/archive_final/",
"__pycache__/",
"*.pyc",
"*.log"
]

existing=""
if gitignore.exists():
    existing=gitignore.read_text()

for x in ignore:
    if x not in existing:
        existing += "\n"+x

gitignore.write_text(existing)


# manifest
manifest={
"time":str(datetime.now()),
"root":str(ROOT.resolve()),
"policy":{
"auto_backup":True,
"protect_backups":True,
"require_commit":True
}
}

(GUARD/"policy.json").write_text(
json.dumps(manifest,indent=2),
encoding="utf8"
)


# initial checkpoint
subprocess.run(["git","add","."])
subprocess.run([
"git",
"commit",
"-m",
"IMA guardian initial checkpoint"
])

