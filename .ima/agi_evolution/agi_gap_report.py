import json
from pathlib import Path

p=Path(".ima/agi_evolution/AGI_MASTER_GAP_MAP.json")

data=json.loads(p.read_text())

print("=== IMA AGI GAP REPORT ===")

for k,v in data["missing_capabilities"].items():
    print(k, ":", v["status"])

print("=== CURRENT CORE ===")

for k,v in data["current_system"].items():
    print(k, ":", "ACTIVE" if v else "MISSING")
