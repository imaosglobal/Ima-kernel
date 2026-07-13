import os
import json
import time

from runtime.file_clock import file_metadata

ROOT = "."

def scan():
    files = []

    for r, d, f in os.walk(ROOT):
        if ".git" in r:
            continue

        for name in f:
            path = os.path.join(r, name)

            if "/node_modules/" in path:
                continue
            if "/.git/" in path:
                continue

            try:
                files.append(file_metadata(path))
            except:
                continue

    return files

def main():
    data = scan()

    index = {
        "ts": time.time(),
        "count": len(data),
        "files": data
    }

    os.makedirs(".ima", exist_ok=True)

    with open(".ima/global_index.json", "w") as f:
        json.dump(index, f, indent=2)

    print("Index rebuilt:", len(data))

if __name__ == "__main__":
    main()
