from pathlib import Path
import json
import hashlib
import datetime


ROOT = Path(".")
OUTPUT = Path(".ima/ima_sync_tree.json")


IGNORE = {
    "node_modules",
    ".git",
    "__pycache__",
    ".next",
    "dist",
}


def hash_file(path):
    try:
        return hashlib.sha256(
            path.read_bytes()
        ).hexdigest()[:16]
    except:
        return None


def scan_tree():

    tree = {
        "timestamp": str(datetime.datetime.now()),
        "root": str(ROOT),
        "modules": {},
        "files": []
    }

    for path in ROOT.rglob("*"):

        if any(x in path.parts for x in IGNORE):
            continue

        if path.is_file():

            entry = {
                "path": str(path),
                "size": path.stat().st_size,
                "hash": hash_file(path)
            }

            tree["files"].append(entry)


            parts = path.parts

            if len(parts) > 1:
                top = parts[0]

                if top not in tree["modules"]:
                    tree["modules"][top] = 0

                tree["modules"][top] += 1


    return tree



def build_sync_report(tree):

    report = {
        "identity": "IMA",
        "status": "synchronized_scan",
        "components": {}
    }


    areas = [
        "founder",
        "languages",
        "product",
        "ima-ui",
        ".ima"
    ]


    for area in areas:

        report["components"][area] = {
            "exists": Path(area).exists(),
            "files":
                tree["modules"].get(area,0)
        }


    return report



tree = scan_tree()

report = build_sync_report(tree)


OUTPUT.parent.mkdir(
    exist_ok=True
)

OUTPUT.write_text(
    json.dumps(
        {
            "tree":tree,
            "report":report
        },
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)



for k,v in report["components"].items():

