from pathlib import Path
import shutil
import time

files=[
"learning/source_router.py",
"learning/world_learning_engine.py",
"learning/world_graph_updater.py",
"learning/knowledge_provenance_connector.py",
"learning/sources/source_generator.py"
]


for f in files:

    p=Path(f)

    if not p.exists():
        continue

    backup=p.with_suffix(".before_import_cleanup.py")
    shutil.copy2(p,backup)

    lines=p.read_text(
        encoding="utf8"
    ).splitlines()

    new=[]
    added=False

    for line in lines:

        if "from learning.sources.html_extractor import extract_text" in line:

            if not added:
                new.append(
                    "from learning.sources.html_extractor import extract_text"
                )
                added=True

            # remove corrupted import line
            if line.strip() == "from learning.sources.html_extractor import extract_text":
                continue

            if "from pathlib from" in line:
                new.append(
                    "from pathlib import Path"
                )
                continue

            if "from learning.source_manager from" in line:
                new.append(
                    "from learning.source_manager import *"
                )
                continue

            continue

        new.append(line)

    p.write_text(
        "\n".join(new)+"\n",
        encoding="utf8"
    )


failed=[]

for f in files:
    import subprocess

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
    for f,e in failed:
else:

