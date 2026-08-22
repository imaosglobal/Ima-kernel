from pathlib import Path
import json
import importlib.util

REGISTRY = Path("kernel/plugins/registry.json")


def load_registry():
    if not REGISTRY.exists():
        return {"plugins": []}

    return json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )


def scan_plugins():
    data = load_registry()

    result = {
        "system": "IMA",
        "loaded": []
    }

    for plugin in data["plugins"]:
        path = Path(plugin["path"])

        result["loaded"].append({
            "name": plugin["name"],
            "exists": path.exists(),
            "status": plugin["status"]
        })

    return result


if __name__ == "__main__":
        scan_plugins(),
        indent=2,
        ensure_ascii=False
    ))
