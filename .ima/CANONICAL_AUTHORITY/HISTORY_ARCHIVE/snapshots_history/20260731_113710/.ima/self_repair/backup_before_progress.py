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


def hash_file(path):
    h=hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def snapshot():

    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    target=SNAP/stamp
    target.mkdir()

    files=[]

    for p in ROOT.rglob("*.py"):
        if any(x in p.parts for x in [".git","node_modules","__pycache__"]):
            continue

        try:
            rel=p.relative_to(ROOT)
            dest=target/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest)

            files.append({
                "file":str(rel),
                "hash":hash_file(p)
            })

        except Exception:
            pass

    return {
        "snapshot":stamp,
        "files":len(files)
    }


def compile_check():

    errors=[]

    for p in ROOT.rglob("*.py"):

        if any(x in p.parts for x in [".git","node_modules","__pycache__"]):
            continue

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

    return errors


def compress_old_snapshots():

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
