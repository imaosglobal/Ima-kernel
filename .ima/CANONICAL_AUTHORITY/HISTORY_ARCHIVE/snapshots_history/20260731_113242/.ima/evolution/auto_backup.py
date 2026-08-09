import shutil
import json
import time
from pathlib import Path


ROOT = Path(".")
BACKUP_DIR = Path(".ima/snapshots/before_change")
LOG = Path(".ima/evolution/backups.json")


def create_backup(files=None):

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    if files is None:
        files = [
            "ima_system.py",
            "ima_kernel.py"
        ]

    copied = []

    for file in files:
        src = Path(file)

        if src.exists():
            dst = BACKUP_DIR / f"{timestamp}_{src.name}"
            shutil.copy(src, dst)
            copied.append(str(dst))


    record = {
        "time": timestamp,
        "files": copied,
        "status": "completed"
    }


    LOG.parent.mkdir(parents=True, exist_ok=True)

    history=[]

    if LOG.exists():
        try:
            history=json.loads(LOG.read_text())
        except:
            history=[]

    history.append(record)

    LOG.write_text(
        json.dumps(history,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )

    return record


if __name__ == "__main__":
    print(create_backup())
