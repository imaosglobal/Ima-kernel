from pathlib import Path
import shutil
import time

print("=== CONNECT ADAPTIVE LEARNING ===")

# backup
targets=[
"learning/sources/source_learning_daemon.py",
"learning/knowledge_runtime_bridge.py"
]

for f in targets:
    p=Path(f)
    b=p.with_suffix(
        f".adaptive_backup_{int(time.time())}.py"
    )
    shutil.copy2(p,b)
    print("[BACKUP]",b)


# add adaptive import to runtime bridge
p=Path("learning/knowledge_runtime_bridge.py")
text=p.read_text(encoding="utf8")

if "knowledge_compactor" not in text:

    text=text.replace(
        "from learning.knowledge_fusion import fuse_sources",
        """from learning.knowledge_fusion import fuse_sources
from learning.knowledge_compactor import compact"""
    )


# compact incoming knowledge before fusion
if "compact(" not in text:

    text=text.replace(
        "sources = collect(question)",
        """sources = collect(question)

    for s in sources:
        if "content" in s:
            s["content"] = compact(s["content"])"""
    )


p.write_text(
    text,
    encoding="utf8"
)


# add safe adaptive cycle call
p=Path(
"learning/sources/source_learning_daemon.py"
)

text=p.read_text(encoding="utf8")

if "adaptive_learning_daemon" not in text:

    text=text.replace(
        "def learning_cycle():",
        """def learning_cycle():

    try:
        from learning.adaptive_learning_daemon import learning_cycle as adaptive_cycle
        adaptive_cycle()
    except Exception as e:
        print("[ADAPTIVE SKIPPED]",e)"""
    )

    p.write_text(
        text,
        encoding="utf8"
    )


print("[COMPILE]")

import subprocess

failed=[]

for f in targets:

    r=subprocess.run(
        [
            "python3",
            "-m",
            "py_compile",
            f
        ],
        capture_output=True,
        text=True
    )

    if r.returncode:
        failed.append((f,r.stderr))


if failed:
    print("[FAILED]")
    for f,e in failed:
        print(f,e)
else:
    print("[CONNECTED]")


print("=== COMPLETE ===")
