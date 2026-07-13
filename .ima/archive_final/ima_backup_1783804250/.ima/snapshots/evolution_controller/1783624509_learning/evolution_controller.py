from pathlib import Path
import json
import time
import py_compile
import shutil

from learning.health_check import health_report
from learning.meta_orchestrator import run_meta_analysis


SNAPSHOT = Path(".ima/snapshots/evolution_controller")
SNAPSHOT.mkdir(parents=True, exist_ok=True)


def snapshot():

    stamp = str(int(time.time()))

    files = [
        "ima.py",
        "ima_system.py",
        "learning",
        "engines"
    ]

    copied=[]

    for item in files:
        src=Path(item)

        if src.exists():

            if src.is_file():
                dst=SNAPSHOT/f"{stamp}_{src.name}"
                shutil.copy(src,dst)
                copied.append(str(dst))

            elif src.is_dir():
                dst=SNAPSHOT/f"{stamp}_{src.name}"
                shutil.copytree(src,dst)
                copied.append(str(dst))

    return copied



def compile_check():

    errors=[]

    for f in Path(".").rglob("*.py"):

        if ".git" in str(f):
            continue

        try:
            py_compile.compile(
                str(f),
                doraise=True
            )

        except Exception as e:
            errors.append({
                "file":str(f),
                "error":str(e)
            })

    return errors



def evolution_cycle():

    print("=== IMA EVOLUTION CONTROLLER ===")

    backup=snapshot()

    print("SNAPSHOT:",len(backup),"items")

    compile_errors=compile_check()

    print(
        "COMPILE ERRORS:",
        len(compile_errors)
    )

    health=health_report()

    failed=[
        x for x in health
        if x["status"]!="ok"
    ]

    print(
        "HEALTH FAILURES:",
        len(failed)
    )


    meta=run_meta_analysis()


    result={
        "time":time.time(),
        "snapshot":backup,
        "compile_errors":compile_errors,
        "health_failed":failed,
        "capabilities":meta["capabilities"],
        "suggestions":meta["suggestions"]
    }


    Path(".ima/evolution_state.json").write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


    print("EVOLUTION STATE SAVED")

    return result



if __name__=="__main__":
    evolution_cycle()
