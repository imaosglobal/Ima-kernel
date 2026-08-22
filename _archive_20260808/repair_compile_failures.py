from pathlib import Path
import shutil
import subprocess
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

    if p.exists():

        backup=p.with_suffix(
            ".before_compile_fix.py"
        )

        shutil.copy2(p,backup)

        text=p.read_text(
            encoding="utf8"
        )

        # remove accidental duplicate imports
        lines=[]
        seen=set()

        for line in text.splitlines():

            if line.startswith("from learning.sources.html_extractor import extract_text"):

                if "extract_text" in seen:
                    continue

                seen.add("extract_text")

            lines.append(line)

        p.write_text(
            "\n".join(lines)+"\n",
            encoding="utf8"
        )



failed=[]

for f in files:

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
        failed.append(
            (f,r.stderr)
        )

if failed:

    for f,e in failed:

else:


