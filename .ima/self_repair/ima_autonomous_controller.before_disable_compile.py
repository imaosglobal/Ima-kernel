

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
SNAP=IMA/"CANONICAL_AUTHORITY/SINGLE_SNAPSHOT"


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

    print("[1/3] CANONICAL MANIFEST SNAPSHOT START", flush=True)

    SNAP.mkdir(parents=True, exist_ok=True)

    manifest = SNAP / "CURRENT_manifest.json"

    files=[]

    INCLUDE=[
        "ima_runtime.py",
        "kernel",
        "runtime",
        "services",
        "connectors",
        "learning",
        "intelligence"
    ]

    for root_part in INCLUDE:

        base=ROOT/root_part

        if not base.exists():
            continue

        for p in base.rglob("*.py"):

            try:
                rel=str(p.relative_to(ROOT))

                files.append({
                    "file": rel,
                    "hash": hash_file(p)
                })

            except Exception:
                continue

    import json

    manifest.write_text(
        json.dumps(
            {
                "snapshot":"CURRENT",
                "files":len(files),
                "manifest":files
            },
            indent=2
        ),
        encoding="utf-8"
    )

    print("[1/3] CANONICAL MANIFEST SNAPSHOT DONE:",len(files),flush=True)

    return {
        "snapshot":"CURRENT",
        "files":len(files)
    }



def compile_check():

    print("[2/3] CANONICAL COMPILE CHECK START", flush=True)

    errors=[]
    count=0

    manifest = SNAP/"CURRENT"

    if not manifest.exists():
        print("NO CANONICAL SNAPSHOT")
        return errors

    for p in manifest.rglob("*.py"):

        try:
            result=subprocess.run(
                ["python3","-m","py_compile",str(p)],
                capture_output=True,
                text=True
            )

            count+=1

            if count % 100 == 0:
                print("compiled:",count,flush=True)

            if result.returncode != 0:
                errors.append({
                    "file":str(p),
                    "error":result.stderr
                })

        except Exception as e:
            errors.append({
                "file":str(p),
                "error":str(e)
            })

    print("[2/3] CANONICAL COMPILE CHECK DONE:",count,flush=True)

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
