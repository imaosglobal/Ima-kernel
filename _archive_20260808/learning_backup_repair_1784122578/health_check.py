from pathlib import Path
import importlib


def check_module(path):

    result = {
        "module": str(path),
        "exists": path.exists(),
        "importable": True,
        "status": "ok"
    }

    try:
        name = str(path).replace("/", ".").replace(".py", "")
        importlib.import_module(name)

    except Exception as e:
        result["importable"] = False
        result["status"] = str(e)

    return result


def health_report():

    reports = []

    for file in Path("learning").glob("*.py"):
        if file.name.startswith("__"):
            continue

        reports.append(check_module(file))

    return reports
