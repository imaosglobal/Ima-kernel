from pathlib import Path
import json
from datetime import datetime


BASE=Path.home()/"ima_kernel"

EVO=Path.home()/".ima/evolution"

OUT=EVO/"system_truth.json"

REGISTRY=BASE/".ima/registry/component_registry.json"


SCAN_DIRS=[
    "connectors",
    "intelligence",
    "learning",
    "memory",
    "runtime",
    "product",
    ".ima"
]


def load(path):

    if path.exists():

        try:
            return json.loads(path.read_text())

        except:
            return {}

    return {}


def save(path,data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def scan_components():

    components=[]

    for folder in SCAN_DIRS:

        path=BASE/folder

        if path.exists():

            files=list(path.rglob("*"))

            py=len(
                [
                    x for x in files
                    if x.suffix==".py"
                ]
            )

            json_files=len(
                [
                    x for x in files
                    if x.suffix==".json"
                ]
            )

            components.append(
                {
                    "name":folder,
                    "path":str(path),
                    "status":"found",
                    "files":len(files),
                    "python_files":py,
                    "json_files":json_files,
                    "checked":datetime.now().isoformat()
                }
            )

    return components



truth=load(OUT)

registry=load(REGISTRY)

components=scan_components()


truth["generated"]=datetime.now().isoformat()

truth["architecture_scan"]={

    "scanned":
    SCAN_DIRS,

    "components_found":
    len(components),

    "components":
    components
}


truth["verified_components"]=components


registry["updated"]=datetime.now().isoformat()

registry["components"]=components


save(
    OUT,
    truth
)

save(
    REGISTRY,
    registry
)


print("SYSTEM TRUTH REGISTRY UPGRADED")
