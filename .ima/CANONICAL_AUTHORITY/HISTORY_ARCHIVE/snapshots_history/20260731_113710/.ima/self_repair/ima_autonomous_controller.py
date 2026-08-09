

HISTORY_EXCLUDE_PATHS = [
    ".ima/self_repair/snapshots",
    ".ima/runtime_snapshots",
    ".ima/canonical_snapshots",
    ".ima/REPAIR_BACKUPS",
    "backup",
    "backups"
]

def is_history_file(path):
    p = str(path)
    return any(x in p for x in HISTORY_EXCLUDE_PATHS)

from pathlib import Path
import json
import shutil
import hashlib
import subprocess
from datetime import datetime


ROOT=Path(".")
IMA=Path(".ima")

STATE=IMA/"self_repair/state.json"
BACKUP=IMA/"self_repair/backups"
REPORT=IMA/"self_repair/controller_report.json"
SNAP=IMA/"self_repair/snapshots"


for p in [BACKUP,SNAP]:
    p.mkdir(parents=True,exist_ok=True)


EXCLUDE_DIRS={
    ".git",
    "node_modules",
    "__pycache__",
    "snapshots",
    "backups"
}


def excluded(path):
    return any(
        part in EXCLUDE_DIRS
        for part in path.parts
    )


def hash_file(path):
    h=hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def snapshot():

    print("[1/3] SNAPSHOT START", flush=True)

    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    target=SNAP/stamp
    target.mkdir()

    files=[]

    count=0

    for p in ROOT.rglob("*.py"):

        if excluded(p):
            continue

        try:
            rel=p.relative_to(ROOT)
            dest=target/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            if excluded(rel):
                continue

            shutil.copy2(p,dest)

            count+=1

            if count > 10000:
                raise RuntimeError(
                    "SNAPSHOT SAFETY LIMIT EXCEEDED"
                )

            if count % 100 == 0:
                print("snapshot files:",count,flush=True)

            files.append({
                "file":str(rel),
                "hash":hash_file(p)
            })

        except Exception:
            pass

    print("[1/3] SNAPSHOT DONE:",len(files),flush=True)

    return {
        "snapshot":stamp,
        "files":len(files)
    }


def compile_check():

    print("[2/3] COMPILE CHECK START",flush=True)

    errors=[]
    count=0

    for p in ROOT.rglob("*.py"):

        if excluded(p):
            continue

        count+=1

        if count % 100 == 0:
            print("compiled:",count,flush=True)

        r=subprocess.run(
            ["python3","-m","py_compile",str(p)],
            capture_output=True,
            text=True
        )

        if r.returncode!=0:
            errors.append({
                "file":str(p),
                "error":r.stderr[-300:]
            })

    print("[2/3] COMPILE CHECK DONE errors:",len(errors),flush=True)

    return errors


def compress_old_snapshots():

    print("[3/3] SNAPSHOT CLEANUP START",flush=True)

    snaps=sorted(SNAP.iterdir())

    removed=0

    while len(snaps)>5:

        old=snaps.pop(0)

        shutil.make_archive(
            str(old),
            "zip",
            old
        )

        shutil.rmtree(old)
        removed+=1

    print("[3/3] SNAPSHOT CLEANUP DONE:",removed,flush=True)

    return removed


def run():

    result={
        "time":datetime.now().isoformat(),
        "actions":[]
    }


    result["actions"].append(
        snapshot()
    )


    errors=compile_check()

    result["compile_errors"]=errors


    result["compressed_snapshots"]=compress_old_snapshots()


    result["status"]=(
        "healthy"
        if not errors
        else "repair_needed"
    )


    REPORT.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


    return result



if __name__=="__main__":

    print(
        json.dumps(
            run(),
            indent=2,
            ensure_ascii=False
        )
    )
