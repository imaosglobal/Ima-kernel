#!/data/data/com.termux/files/usr/bin/bash

set -e

cd "$HOME/ima_kernel"

echo "=== IMA PRODUCT READINESS AUDIT ==="

mkdir -p .ima/governance


python3 - <<'PY'
import json
import time
from pathlib import Path


checks = {

"Android":
[
"android",
"gradle",
"apk"
],

"UI":
[
"frontend",
"src",
"app",
"components",
"react"
],

"API":
[
"api",
"server",
"gateway"
],

"Identity":
[
"user",
"auth",
"profile",
"login"
],

"Security":
[
"safety",
"security",
"permission",
"policy"
],

"Voice":
[
"voice",
"audio",
"speech"
],

"Child":
[
"child",
"kid",
"family",
"parent"
],

"Device":
[
"device",
"iot",
"bluetooth",
"robot"
],

"Deployment":
[
"docker",
"deploy",
"cloud",
"vercel",
"netlify"
]

}


root=Path(".")

files=[
str(x).lower()
for x in root.rglob("*")
if x.is_file()
and ".git" not in str(x)
and ".ima/snapshots" not in str(x)
]


result={}

for name,patterns in checks.items():

    found=[]

    for f in files:
        if any(p in f for p in patterns):
            found.append(f)

    result[name]={
        "status":
        "FOUND" if found else "MISSING",
        "count":
        len(found),
        "examples":
        found[:5]
    }


registry={

"system":"IMA",

"status":
"PRODUCT_READINESS_AUDIT_COMPLETE",

"canonical_brain":
"learning/meta_orchestrator.py",

"canonical_orchestrator":
"learning/module_registry.py",

"checks":
result,

"time":
time.time()

}


Path(
".ima/governance/product_readiness_report.json"
).write_text(
json.dumps(
registry,
indent=2,
ensure_ascii=False
),
encoding="utf-8"
)


for k,v in result.items():
        k,
        ":",
        v["status"],
        "(",
        v["count"],
        ")"
    )


"PRODUCT REPORT SAVED"
)

PY


echo
echo "[1] Canonical system check"

python3 - <<'PY'

from learning.brain_guard import verify_brain

verify_brain(
"learning/meta_orchestrator.py"
)

"CANONICAL BRAIN OK"
)

PY


echo
echo "[2] Existing governance"

ls .ima/governance/*registry*.json 2>/dev/null || true


echo
echo "[3] Final report"

cat .ima/governance/product_readiness_report.json


echo
echo "=== IMA PRODUCT READINESS COMPLETE ==="

