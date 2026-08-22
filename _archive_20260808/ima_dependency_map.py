from pathlib import Path
import json
import re
import datetime

ROOT=Path(".")
OUT=Path(".ima/ima_dependency_map.json")

IGNORE={
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    ".next"
}

patterns=[
    r"from\s+([a-zA-Z0-9_\.]+)",
    r"import\s+([a-zA-Z0-9_\.]+)",
]


modules={}

for path in ROOT.rglob("*.py"):

    if any(x in path.parts for x in IGNORE):
        continue

    try:
        text=path.read_text(
            encoding="utf-8"
        )
    except:
        continue


    imports=[]

    for pattern in patterns:
        imports += re.findall(
            pattern,
            text
        )


    modules[str(path)] = {
        "imports":sorted(
            list(set(imports))
        )
    }


result={
    "identity":"IMA",
    "created":str(datetime.datetime.now()),
    "python_modules":modules,
    "count":len(modules)
}


OUT.write_text(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


