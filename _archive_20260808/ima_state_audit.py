from pathlib import Path
import json
import subprocess

ROOT=Path(".")


# core files
checks=[
".ima",
"learning",
"learning/sources",
"learning/knowledge_runtime_bridge.py",
"learning/knowledge_fusion.py",
"learning/sources/source_learning_daemon.py",
"learning/adaptive_learning_daemon.py",
"learning/learning_policy.json",
]

for c in checks:
    p=Path(c)
        "[OK]" if p.exists() else "[MISSING]",
        c
    )

failed=[]

for p in ROOT.rglob("*.py"):
    if "backup" in str(p):
        continue

    r=subprocess.run(
        [
            "python3",
            "-m",
            "py_compile",
            str(p)
        ],
        capture_output=True,
        text=True
    )

    if r.returncode:
        failed.append(str(p))

if failed:
    for f in failed:
else:


try:
    from learning.source_manager import source_status

    for s in source_status():

except Exception as e:


try:
    from learning.knowledge_runtime_bridge import ask_knowledge

    for q in [
        "IMA",
        "physics",
        "NOAA climate science"
    ]:
        r=ask_knowledge(q)

except Exception as e:


