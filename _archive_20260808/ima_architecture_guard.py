from pathlib import Path
import json
import time

ROOT = Path(".")
REGISTRY = ROOT / ".ima/governance/canonical_architecture.json"
REPORT = ROOT / ".ima/governance/architecture_guard_report.json"

def load_registry():
    if not REGISTRY.exists():
        raise RuntimeError("Missing canonical architecture registry")
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def scan():
    data = load_registry()

    result = {
        "time": time.time(),
        "system": "IMA",
        "state": "GUARDED",
        "canonical": data["canonical_components"],
        "checks": []
    }

    for name, path in data["canonical_components"].items():
        p = ROOT / path
        result["checks"].append({
            "component": name,
            "path": path,
            "exists": p.exists()
        })

    REPORT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return result

if __name__ == "__main__":
    print("=== IMA ARCHITECTURE GUARD ===")

    result = scan()

    missing = []

    for item in result["checks"]:
        status = "OK" if item["exists"] else "MISSING"
        print(
            item["component"],
            status,
            item["path"]
        )

        if not item["exists"]:
            missing.append(item["component"])

    if missing:
        print("WARNING:", missing)
    else:
        print("ALL CANONICAL COMPONENTS VERIFIED")

    print("GUARD REPORT:", REPORT)
