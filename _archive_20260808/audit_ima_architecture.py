from pathlib import Path
import json

checks = {
"entrypoints": [],
"orchestrators": [],
"event_bus": [],
"runtime": [],
"governance": [],
}

for f in Path(".").rglob("*"):
    if not f.is_file():
        continue

    s=str(f).lower()

    if "entrypoint" in s:
        checks["entrypoints"].append(str(f))

    if "orchestrator" in s:
        checks["orchestrators"].append(str(f))

    if "event" in s or "bus" in s:
        checks["event_bus"].append(str(f))

    if "runtime" in s:
        checks["runtime"].append(str(f))

    if "governance" in s:
        checks["governance"].append(str(f))

print(json.dumps(checks,indent=2,ensure_ascii=False))
