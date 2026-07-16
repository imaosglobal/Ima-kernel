import importlib


ALLOWED_TRUST = [
    "high",
    "medium"
]


def validate_source(source):

    if not source.get("enabled"):
        return False

    if source.get("trust") not in ALLOWED_TRUST:
        return False

    if not source.get("module"):
        return False

    if not source.get("function"):
        return False

    try:
        module = importlib.import_module(
            source["module"]
        )

        handler = getattr(
            module,
            source["function"]
        )

        if not callable(handler):
            return False

    except Exception:
        return False

    return True
