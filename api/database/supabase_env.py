import os
from pathlib import Path

def load_env():
    p=Path(".env.production")

    if not p.exists():
        return

    for line in p.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1)
            os.environ.setdefault(k,v)

load_env()
