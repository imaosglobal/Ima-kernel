import json
import importlib
from pathlib import Path

from learning.sources.source_validator import validate_source


def load_sources(registry):

    path = Path(
        "learning/sources/registry.json"
    )

    data=json.loads(
        path.read_text(
            encoding="utf8"
        )
    )

    loaded=[]

    for source in data.get("sources",[]):

        if not validate_source(source):
            continue

        try:

            module=importlib.import_module(
                source["module"]
            )

            handler=getattr(
                module,
                source["function"]
            )

            registry.register(
                source["name"],
                handler,
                priority=source["priority"]
            )

            loaded.append(
                source["name"]
            )

        except Exception:
            pass

    return loaded
