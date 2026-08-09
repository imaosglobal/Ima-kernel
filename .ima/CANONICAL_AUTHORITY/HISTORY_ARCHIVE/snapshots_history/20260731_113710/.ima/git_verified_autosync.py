import os, subprocess, time, hashlib, signal
from pathlib import Path

ROOT=Path.home()/ "ima_kernel"
LOCK=ROOT/".ima/.git_autosync.lock"
BOOT=ROOT/".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py"

def run(cmd):
    return subprocess.run(cmd,cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0

def tracked():
    r=subprocess.run(["git","ls-files","-m"],cwd=ROOT,text=True,capture_output=True)
    return r.stdout.strip()

def cleanup(signum=None, frame=None):
    LOCK.unlink(missing_ok=True)
    if signum:
        raise SystemExit(128 + signum)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

def main():
    if LOCK.exists():
        return
    LOCK.write_text(str(os.getpid()))
    try:
        last=""
        while True:
            current=tracked()
            if current and current!=last:
                last=current
                ok=(
                    run(["python","-m","compileall","-q","kernel",".ima/CANONICAL_AUTHORITY",".ima/agi_evolution"])
                    and run(["python",str(BOOT)])
                )
                if ok:
                    run(["git","add"]+current.splitlines())
                    if run(["git","commit","-m","auto: verified system update"]):
                        run(["git","push"])
            time.sleep(10)
    finally:
        LOCK.unlink(missing_ok=True)

main()
