import json
from pathlib import Path
from learning.sources.source_generator import generate_source

REGISTRY = Path("learning/sources/registry.json")
CANDIDATES = Path("learning/sources/candidates.json")


def promote():

    registry=json.loads(
        REGISTRY.read_text(encoding="utf8")
    )

    candidates=json.loads(
        CANDIDATES.read_text(encoding="utf8")
    )

    existing=set(
        (
            x.get("name"),
            x.get("module","")
        )
        for x in registry["sources"]
    )

    added=[]

    for c in candidates:

        if c.get("status")!="approved":
            continue

        module=c.get("module")

        if not module:
            module=generate_source(
                c["name"],
                c["url"]
            )

            c["module"]=module


        key=(c["name"],module)

        if key in existing:
            continue


        registry["sources"].append(
            {
                "name":c["name"],
                "module":module,
                "function":"search",
                "priority":80,
                "enabled":True,
                "trust":"high"
            }
        )

        added.append(c["name"])


    REGISTRY.write_text(
        json.dumps(
            registry,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )


    CANDIDATES.write_text(
        json.dumps(
            candidates,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )


    return added
