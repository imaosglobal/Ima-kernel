import subprocess
import time
from pathlib import Path

API = Path("api/server.py")

def start_api():
    if not API.exists():
        return False

    subprocess.Popen(
        ["python3", str(API)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(2)
    return True

if __name__ == "__main__":
    print("[API BOOT]", start_api())
