from pathlib import Path
import subprocess
import time

ROOT = Path(".")
WATCH = [
    "learning",
    "ima",
    "api",
    "runtime",
]

def snapshot():
    files={}
    for folder in WATCH:
        p=Path(folder)
        if p.exists():
            for f in p.rglob("*"):
                if f.is_file():
                    files[str(f)] = f.stat().st_mtime
    return files


def cycle():
    print("=== FUTURE GUARDIAN CYCLE ===")

    subprocess.run(
        ["python3","ima_guardian_master.py"],
        text=True
    )


old=snapshot()

while True:
    time.sleep(20)

    new=snapshot()

    if new != old:
        print("[CHANGE DETECTED]")
        cycle()
        old=new
