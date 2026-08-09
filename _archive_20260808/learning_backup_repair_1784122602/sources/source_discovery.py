import json
from pathlib import Path
import importlib


REGISTRY = Path(
    "learning/sources/registry.json"
)


def inspect_source(name, module, function):

    result = {
        "name": name,
        "module": module,
        "function": function,
        "enabled": False,
        "trust": "unknown",
        "priority": 0,
        "status": "pending"
    }


    try:
        mod = importlib.import_module(module)

        handler = getattr(
            mod,
            function
        )

        if callable(handler):
            result["status"] = "valid"
            result["trust"] = "medium"

    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)


    return result



def propose_source(
    name,
    module,
    function,
    priority=50
):

    result = inspect_source(
        name,
        module,
        function
    )

    result["priority"] = priority


    data=json.loads(
        REGISTRY.read_text(
            encoding="utf8"
        )
    )


    data["sources"].append(
        result
    )


    REGISTRY.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )


    return result
