from pathlib import Path
import json
import subprocess

ROOT=Path(".")

print("=== IMA STATE AUDIT ===")

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

print("\n[CORE STRUCTURE]")
for c in checks:
    p=Path(c)
    print(
        "[OK]" if p.exists() else "[MISSING]",
        c
    )

print("\n[PYTHON HEALTH]")
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
    print("[FAILED]")
    for f in failed:
        print("-",f)
else:
    print("[ALL PYTHON OK]")


print("\n[LEARNING SOURCES]")
try:
    from learning.source_manager import source_status

    for s in source_status():
        print("-",s)

except Exception as e:
    print("[ERROR]",e)


print("\n[KNOWLEDGE TEST]")
try:
    from learning.knowledge_runtime_bridge import ask_knowledge

    for q in [
        "IMA",
        "physics",
        "NOAA climate science"
    ]:
        r=ask_knowledge(q)
        print("\nQUERY:",q)
        print("SOURCE:",r.get("source"))
        print("CONF:",r.get("confidence"))

except Exception as e:
    print("[KNOWLEDGE ERROR]",e)


print("\n=== AUDIT COMPLETE ===")
