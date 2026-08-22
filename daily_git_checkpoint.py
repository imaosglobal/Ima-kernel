import subprocess
from datetime import datetime
from pathlib import Path

repo=Path.home()/ "ima_kernel"

subprocess.run(
    ["git","add","-A"],
    cwd=repo
)

status=subprocess.check_output(
    ["git","status","--porcelain"],
    cwd=repo
).decode()

if status.strip():

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"IMA daily checkpoint {datetime.now().isoformat()}"
        ],
        cwd=repo
    )


else:
